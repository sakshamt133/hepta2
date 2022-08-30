from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


def profile_pic_upload(instance, filename):
    ext = filename.split(".")[-1]
    return f"profile/{instance.id}/{uuid4().hex}.{ext}"


class Accounts(AbstractUser):
    """
    Custom user model for storing user related data
    """

    USER_TYPE_CHOICES = (
        (1, "Doctor"),
        (2, "Patient"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="email address")
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    # User Information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=profile_pic_upload, blank=True, null=True)
    address_line1 = models.CharField(max_length=100)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=50)
    address_country = models.CharField(max_length=50)
    address_pin = models.CharField(max_length=6)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_doctor(self):
        return self.user_type == 1

    def __str__(self):
        return self.email
