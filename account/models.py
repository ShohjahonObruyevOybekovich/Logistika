from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import UserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, blank=True, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_pics/', null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

class Role(models.Model):
    class RoleName(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'

    name = models.CharField(
        max_length=5,
        choices=RoleName.choices,
        default=RoleName.USER,
    )

    def __str__(self):
        return self.get_name_display()

class UserRole(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} - {self.role.get_name_display()}"
