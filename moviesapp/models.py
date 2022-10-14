import uuid
from django.db import models
from django.utils import timezone

# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    PermissionsMixin,
    BaseUserManager,
    AbstractBaseUser,
)


class UserManager(BaseUserManager):
    def _create_user(
        self, email, password, is_active, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, True, **extra_fields)
        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=80, blank=True)
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=30, blank=True)
    last_name = models.CharField("last name", max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=20, default="admin")

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Collection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True)
    user_id = models.ForeignKey(
        User,
        to_field="id",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    coll_id = models.ForeignKey(
        Collection,
        to_field="id",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class UserVisit(models.Model):
    endpoint = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.CharField(max_length=20, null=True)
    request_time = models.DateTimeField(auto_now=True)
