from django.contrib.auth.models import AbstractBaseUser, UserManager
from ..utility.models import *
from django.db import models
from .enums import Roles
from django.contrib.auth.models import PermissionsMixin


class MyUserManager(UserManager):

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = MyUser(
            username=email,
            email=email,
            is_active=True,
            is_superuser=True,
            is_staff=True,
            role=Roles.ADMIN.value
        )
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, TimestampMixin, PermissionsMixin):
    username = models.CharField(max_length=255, null=False, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    second_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    # remember_token = models.CharField(max_length=255, default=None, null=True)
    role = models.IntegerField(choices=Roles.choices(), default=Roles.USER.value, null=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    pay_zakyat = models.BooleanField(default=False, null=False)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Partner(TimestampMixin):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'


class PasswordResets(TimestampMixin):
    email = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = 'Password reset'
        verbose_name_plural = 'Password resets'
