# Create your views here.

from django.contrib.auth import get_user_model, authenticate
from passlib.context import CryptContext
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserLoginSerializer, UserListSerializer, UserSerializer
from .serializers import UserCreateSerializer, UserUpdateSerializer

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


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
            return Response({'success': False, 'message': 'This phone number is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before creating the user
        user = User.objects.create(
            phone=phone,
        )
        user.set_password(password)  # Hash the password
        user.save()

        return Response({'success': True, 'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
# class ConfirmationCodeAPIView(GenericAPIView):
#     serializer_class = ConfirmationCodeSerializer
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         # username = request.data.get('username')
#         confirm_code = request.data.get('confirmation_code')
#         cached_data = cache.get(email)
#         print(email)
#         print(confirm_code)
#         print(cached_data)
#         if cached_data and confirm_code == cached_data['confirmation_code']:
#             password = cached_data['password']
#
#             if User.objects.filter(email=email).exists():
#                 return Response({'success': False, 'message': 'This email already exists!'}, status=400)
#             # if User.objects.filter(username=cached_data['username']).exists():
#             #     return Response({'success': False, 'message': 'This username already exists!'}, status=400)
#             else:
#                 User.objects.create_user(
#                     email=email,
#                     # username=cached_data['username'],
#                     password=password,
#                 )
#                 return Response({'success': True})
#         else:
#             return Response({'message': 'The entered code is not valid! '}, status=status.HTTP_400_BAD_REQUEST)

# class PasswordResetRequestView(GenericAPIView):
#     serializer_class = PasswordResetRequestSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#             uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
#             token = default_token_generator.make_token(user)
#             reset_link = f"http://127.0.0.1:8000/auth/reset-password/"
#             send_forget_password.delay(email, reset_link)
#             return Response({'success': 'Password reset link sent'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PasswordResetView(GenericAPIView):
#     serializer_class = PasswordResetLoginSerializer
#
#     def post(self, request, uid, token):
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             new_password = serializer.validated_data['new_password']
#
#             try:
#                 user = User.objects.get(pk=uid)
#
#                 print(default_token_generator.check_token(user, token))
#
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
#                 # Log the error message for debugging
#                 print(f"Error occurred while decoding uid: {e}")
#                 user = None
#
#             if user is not None:
#                 # Reset the user's password
#                 user.set_password(new_password)
#                 user.save()
#                 return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_object(self):
        return self.request.user  # Get the current user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, id=None):
        try:
            # Fetch the user by the given ID or raise a 404 error if not found
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Serialize the user data
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)