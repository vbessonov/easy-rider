from dataclasses import dataclass
from enum import IntFlag

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class RoleEnum(IntFlag):
    USER = 1
    MANAGER = 2
    ADMIN = 4


class UserManager(BaseUserManager):
    def _create_user(self, email: str, is_superuser: bool, password=None, **extra_fields) -> 'User':
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password=None, **extra_fields) -> 'User':
        """
        Creates and saves a user with the given email, and password.
        """

        return self._create_user(email, False, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields) -> 'User':
        """
        Creates and saves a superuser with the given email, and password.
        """

        return self._create_user(email, True, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Class extending built-in User model.
    """

    ROLE_CHOICES = (
        (int(RoleEnum.USER), 'User'),
        (int(RoleEnum.MANAGER), 'Manager'),
        (int(RoleEnum.ADMIN), 'Admin'),
    )

    password = models.CharField('password', max_length=128, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='email address', max_length=255, blank=False, null=False, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default=int(RoleEnum.USER))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    @property
    def is_staff(self):
        """
        Returns a boolean value indicating whether the current user has access to the admin site.
        :return: boolean value indicating whether the current user has access to the admin site
        """

        return self.is_superuser

    def __str__(self) -> str:
        return self.email


@dataclass
class CurrentUser:
    """
    Dummy model which is used by /auth/user endpoint
    """

    user: settings.AUTH_USER_MODEL


class Trip(models.Model):
    """
    Trip model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.CharField(max_length=120, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
