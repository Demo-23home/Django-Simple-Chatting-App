from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None) -> "User":
        if not email:
            raise ValueError("An email is required !")

        if not password:
            raise ValueError("A password is required")

        email = self.normalize_email(email)

        user = self.model(email=email)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email: str, password: str | None = None) -> "User":
        if not email:
            raise ValueError("An email is required!")

        if not password:
            raise ValueError("A password is required !")

        user = self.create_user(email, password)

        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    country = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}"
