from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from typing import Literal

class CustomUserManager(BaseUserManager):
    """
    Custom User Manager used for handling Custom User Model which
    has one field less than the Django default Base User, here the 
    username is removed
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save the user with the given email and password
        """
        if not email: raise ValueError("Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_user(self, email, password = None, **extra_fields):
        """
        Create and save regular user with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super User is missing is_staff permission")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super User is missing is_superuser permission")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User Model, similar to Django defaut User Mode, except the default "USERNAME_FIELD"
    is set to "email"
    """
    USERNAME_FIELD = "email"

    username = None
    email = models.EmailField(_("email address"), unique = True, null = True)
    first_name = models.CharField(max_length = 30, blank = True)
    last_name = models.CharField(max_length = 30, blank = True)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

