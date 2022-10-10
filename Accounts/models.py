from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager, PermissionManager,PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.db.models.deletion import CASCADE
from django.core.mail import send_mail
from django.db import models
import uuid

GENDER_OPTIONS = (("Male","Male"),("Female","Female"))


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user



class AccountModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('Email Address'), unique=True)
    username = models.CharField(verbose_name=_("Username"),max_length=150, blank=True)
    phone = models.CharField(verbose_name=_("Phone Number"),max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()

    send_mail = models.BooleanField(default=False)
    nationality =CountryField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(subject,message,'l@1.com',[self.email],fail_silently=False,)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        context ={
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
        return context
    def __str__(self):
        return self.name
