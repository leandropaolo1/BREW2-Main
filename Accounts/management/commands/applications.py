from Accounts.models import CustomAccountManager, AccountModel
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.conf import settings


class OAuthPEN4:
    def generate_instance(self):
        account_instance = AccountModel.objects.filter(
            username="pen4-application").first()

        if not account_instance:
            account_instance = CustomAccountManager().create_user(
                password=settings.PEN4_ACCOUNT_PASSWORD,
                phone=settings.PEN4_ACCOUNT_PHONE,
                email=settings.PEN4_ACCOUNT_EMAIL,
                first_name="pen4-application",
                username="pen4-application",
                last_name="pen4-application")

        application_instance = Application.objects.filter(
            client_id=settings.PEN4_APPLICATION_ID).first()

        if application_instance:
            return

        return Application.objects.create(
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_secret=settings.PEN4_APPLICATION_SECRET,
            client_type=Application.CLIENT_CONFIDENTIAL,
            client_id=settings.PEN4_APPLICATION_ID,
            name="PEN4_APPLICATION",
            user=account_instance,
            redirect_uris="")


class OAuthPEN5:
    def generate_instance(self):
        account_instance = AccountModel.objects.filter(
            username="pen5-application").first()

        if not account_instance:
            account_instance = CustomAccountManager().create_user(
                password=settings.PEN5_ACCOUNT_PASSWORD,
                phone=settings.PEN5_ACCOUNT_PHONE,
                email=settings.PEN5_ACCOUNT_EMAIL,
                first_name="pen5-application",
                username="pen5-application",
                last_name="pen5-application")

        application_instance = Application.objects.filter(
            client_id=settings.PEN5_APPLICATION_ID).first()

        if application_instance:
            return

        return Application.objects.create(
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_secret=settings.PEN5_APPLICATION_SECRET,
            client_type=Application.CLIENT_CONFIDENTIAL,
            client_id=settings.PEN5_APPLICATION_ID,
            name="PEN5_APPLICATION",
            user=account_instance,
            redirect_uris="")


class OAuthPEN6:
    def generate_instance(self):
        account_instance = AccountModel.objects.filter(
            username="pen6-application").first()

        if not account_instance:
            account_instance = CustomAccountManager().create_user(
                password=settings.PEN6_ACCOUNT_PASSWORD,
                phone=settings.PEN6_ACCOUNT_PHONE,
                email=settings.PEN6_ACCOUNT_EMAIL,
                first_name="pen6-application",
                username="pen6-application",
                last_name="pen6-application")

        application_instance = Application.objects.filter(
            client_id=settings.PEN6_APPLICATION_ID).first()

        if application_instance:
            return

        return Application.objects.create(
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_secret=settings.PEN6_APPLICATION_SECRET,
            client_type=Application.CLIENT_CONFIDENTIAL,
            client_id=settings.PEN6_APPLICATION_ID,
            name="PEN6_APPLICATION",
            user=account_instance,
            redirect_uris="")


class Command(BaseCommand):
    def generate(self):
        OAuthPEN4().generate_instance()
        OAuthPEN5().generate_instance()
        OAuthPEN6().generate_instance()

    def handle(self, *args, **kwargs):
        self.generate()
