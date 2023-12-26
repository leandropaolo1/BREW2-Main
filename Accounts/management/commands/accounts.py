from Accounts.models import CustomAccountManager, AccountModel
from django.core.management.base import BaseCommand
from django.conf import settings
import json
import uuid


class AccountData:
    def generate_instances(self):
        with open("_docs/accounts.json", "r") as file:
            self.account_data = json.load(file)
        account_private_uuid = uuid.UUID(self.account_data.get("private_uuid"))
        account_instance = AccountModel.objects.filter(
            id=account_private_uuid)
        if not account_instance:
            if not AccountModel.objects.filter(is_superuser=True).first():
                CustomAccountManager().create_superuser(
                    username=self.account_data.get("username"),
                    password=settings.DJANGO_SUPERUSER_PASSWORD,
                    phone=self.account_data.get("phone"),
                    email=self.account_data.get("email"),
                    id=account_private_uuid)

    account_test_uuid = uuid.UUID(settings.PEN_TEST_PRIVATE_UUID)
    account_instance = AccountModel.objects.filter(
        id=account_test_uuid).first()
    if not account_instance:
        CustomAccountManager().create_user(
            username=settings.PEN_TEST_USERNAME,
            password=settings.PEN_TEST_PASSWORD,
            phone=settings.PEN_TEST_PHONE,
            email=settings.PEN_TEST_EMAIL,
            id=account_test_uuid)


class Command(BaseCommand):
    def generate(self):
        try:
            AccountData().generate_instances()
        except Exception as e:
            print(e)
            pass

    def handle(self, *args, **kwargs):
        self.generate()
