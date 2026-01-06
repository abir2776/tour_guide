import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .choices import Status, UserGender, UserRole
from .managers import CustomUserManager

logger = logging.getLogger(__name__)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True, editable=False)
    phone = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Phone Number", blank=True, null=True
    )
    mobile = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Mobile Number", blank=True, null=True
    )
    whatsapp = PhoneNumberField(
        unique=True,
        db_index=True,
        verbose_name="What's app Number",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.UNKNOWN,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"UID: {self.uid}, Phone: {self.phone}"

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()
