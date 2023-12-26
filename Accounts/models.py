from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from Accounts.mixins import AccountModelMixin
from django.conf import settings
from django.db import models
import uuid


from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager)


class CustomAccountManager(BaseUserManager):
    def create_superuser(
            self,
            username,
            email,
            password,
            **other_fields):

        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **other_fields)

    def create_user(
            self,
            email,
            username,
            password,
            **other_fields):
        try:
            email = self.normalize_email(email)
            phone = str(phone)

            account_instance = AccountModel(
                username=username,
                phone=phone,
                email=email,
                **other_fields)

            account_instance.set_password(password)
            account_instance.save()
            return account_instance
        except Exception:
            return None


class AccountModel(AbstractBaseUser, PermissionsMixin, AccountModelMixin):
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']
    USERNAME_FIELD = 'email'

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    public_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    private_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=255,
        unique=True,
        blank=False,
        null=False)

    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=255,
        unique=True,
        blank=False,
        null=False)

    country = CountryField(
        verbose_name=_("Country"),
        default="SV",
        unique=False,
        blank=False,
        null=False)

    email_confirmation_sent = models.BooleanField(
        default=False)

    email_confirmed = models.BooleanField(
        default=False)

    is_active = models.BooleanField(
        default=True)

    is_staff = models.BooleanField(
        default=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    objects = CustomAccountManager()

    @property
    def joined(self):
        return self.date_created.strftime("%B %d, %Y %I:%M %p")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Account Models"
        verbose_name = "Account Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.username
