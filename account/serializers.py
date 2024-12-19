from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import CustomUser

User = get_user_model()



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password')

class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetLoginSerializer(serializers.Serializer):
    new_password = serializers.CharField()



from account.permission import EmailAuthBackend
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=20, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:

            user = EmailAuthBackend().authenticate(request=self.context.get('request'),
                                email=email, password=password)
            print(user)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs




class UserUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    password = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email','full_name','image', 'phone', 'password','telegram_username']

    def validate(self, attrs):
        user = self.instance  # Get the user instance
        if 'password' in attrs:
            user.set_password(attrs['password'])
            user.save()
        return attrs

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"image",'email',"full_name", 'password','telegram_username']
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('image',"full_name", 'email',  'phone','telegram_username')