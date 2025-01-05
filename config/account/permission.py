from django.contrib.auth.backends import BaseBackend, UserModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
# from .models import UserRole

#
# class IsAdminPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             admin_role = UserRole.objects.get(user=request.user).role.name
#         except UserRole.DoesNotExist:
#             return False
#         return admin_role.lower() == "admin"

from django.contrib.auth import get_user_model

from account.models import CustomUser


class PhoneAuthBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None):
        print(f"Attempting authentication for phone: {phone}")
        try:
            user = CustomUser.objects.get(phone=phone)
            if user.check_password(password):
                print("Authentication successful")
                return user
            else:
                print("Invalid password")
        except CustomUser.DoesNotExist:
            print("User does not exist")
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

class CanDeleteUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff