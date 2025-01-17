from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .managers import MyUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    activation_code = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code
        return self.activation_code

    def __str__(self):
        return f'{self.email}'

class UserResetPasswordToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)