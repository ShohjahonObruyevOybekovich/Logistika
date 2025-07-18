# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from passlib.context import CryptContext
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserLoginSerializer, UserListSerializer, UserSerializer
from .serializers import UserCreateSerializer, UserUpdateSerializer

User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class RegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        # Validate incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        # Check if the phone number already exists
        if User.objects.filter(phone=phone).exists():
            return Response({'success': False, 'message': 'This phone number is already registered.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before creating the user
        user = User.objects.create(
            phone=phone,
        )
        user.set_password(password)  # Hash the password
        user.save()

        return Response({'success': True, 'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = User.objects.all().order_by('id')

    serializer_class = UserListSerializer


@extend_schema(
    request=UserLoginSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    }
)
class CustomAuthToken(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        # Validate serializer data
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get the validated user
        user = serializer.validated_data.get('user')
        if not user:
            raise AuthenticationFailed("Invalid credentials or user does not exist.")

        # Generate Refresh and Access Tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user.pk,
            'phone': user.phone,
        }, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found."})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  # Get the pk from the URL
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(
                    {"error": "This phone number is already in use."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            # Get refresh token from request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, id=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Serialize the user data
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
