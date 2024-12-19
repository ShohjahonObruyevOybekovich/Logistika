from django.contrib.auth.backends import BaseBackend, UserModel
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

class EmailAuthBackend:
    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
