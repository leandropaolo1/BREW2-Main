from Accounts.models import AccountModel, CustomAccountManager
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from django.core.cache import cache
from django.conf import settings
from faker import Faker
import requests
import datetime
import hashlib
import uuid


class MockCustomAuth1(BaseAuthentication):
    def authenticate(self, request):
        return (None, (uuid.uuid4(), Faker().email(), {}))

    def has_permission(self, request, view):
        return True

    def authenticate_header(self, request):
        return 'MockCustomAuth1'


class CustomAuth1(BaseAuthentication, BasePermission):
    def authenticate(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            auth_token = auth_header
            hashed_token = hashlib.sha256(auth_token.encode()).hexdigest()

            response = requests.post(
                url=settings.PEN3_TOKEN_VERIFY1,
                data={'token': auth_token},
                timeout=5)

            serialized_data = response.json()
            request.session['auth_response'] = serialized_data
            timestamp = serialized_data.get('expiration')
            if timestamp is None:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            expired = datetime.datetime.fromtimestamp(
                timestamp) <= datetime.datetime.now()

            private_uuid = serialized_data.get('private_uuid')

            if not private_uuid or response.status_code != 200 or expired:
                raise AuthenticationFailed(
                    'Authentication failed. Invalid token or expired token.')

            cache.set(hashed_token, (private_uuid, timestamp))
            return (None, (private_uuid, auth_header))

        except AuthenticationFailed:
            raise AuthenticationFailed(
                'Authentication failed. Invalid token or expired token.')

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def has_permission(self, request, view):
        try:
            auth_response = request.session.get('auth_response')

            if auth_response:

                timestamp = auth_response.get('expiration')
                expired = datetime.datetime.fromtimestamp(
                    timestamp) <= datetime.datetime.now()
                return not expired

            return False

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def authenticate_header(self, request):
        return 'CustomAuth1'


class CustomAuth2(BaseAuthentication, BasePermission):
    def authenticate(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            auth_token = auth_header
            hashed_token = hashlib.sha256(auth_token.encode()).hexdigest()

            response = requests.post(
                url=settings.PEN3_TOKEN_VERIFY2,
                data={'token': auth_token},
                timeout=5)

            serialized_data = response.json()
            request.session['auth_response'] = serialized_data
            timestamp = serialized_data.get('expiration')
            if timestamp is None:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            expired = datetime.datetime.fromtimestamp(
                timestamp) <= datetime.datetime.now()
            readable_time = datetime.datetime.fromtimestamp(timestamp)
            expired = readable_time >= datetime.datetime.now()

            private_uuid = serialized_data.get('private_uuid')
            account_email = serialized_data.get('account_email')

            if not private_uuid or response.status_code != 200 or expired == False or not account_email:
                raise AuthenticationFailed(
                    'Authentication failed. Invalid token or expired token.')

            cache.set(hashed_token, (timestamp, private_uuid, account_email))
            return (None, (private_uuid, account_email, auth_header))

        except AuthenticationFailed as e:
            raise e

        except TypeError:
            raise AuthenticationFailed('Internal server error.')

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def has_permission(self, request, view):
        try:
            auth_response = request.session.get('auth_response')

            if auth_response:

                timestamp = auth_response.get('expiration')
                expired = datetime.datetime.fromtimestamp(
                    timestamp) <= datetime.datetime.now()
                return not expired

            return False

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def authenticate_header(self, request):
        return 'CustomAuth2'


class CustomAuth3(BaseAuthentication, BasePermission):
    def _make_request(self, authentication_token):
        try:
            response = requests.post(
                url=settings.PEN3_TOKEN_VERIFY1,
                data={'token': authentication_token},
                timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            return None

    def authenticate(self, request):
        try:
            authentication_token = request.META.get('HTTP_AUTHORIZATION')
            if not authentication_token:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            response_data = self._make_request(
                authentication_token)

            timestamp = response_data.get('expiration', None)
            if timestamp is None:
                raise AuthenticationFailed(
                    'Authentication credentials were not provided.')

            expired = datetime.datetime.fromtimestamp(
                timestamp) <= datetime.datetime.now()
            readable_time = datetime.datetime.fromtimestamp(timestamp)
            expired = readable_time >= datetime.datetime.now()
            private_uuid = response_data.get('private_uuid', False)

            params = [
                response_data.status_code == 200,
                private_uuid != False,
                expired == False]

            if False in params:
                raise AuthenticationFailed(
                    'Authentication failed. Invalid token or expired token.')

            account_instance = CustomAccountManager().createAccountInstance(
                private_uuid=private_uuid)

            return (account_instance)

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def has_permission(self, request, view):
        try:
            auth_response = request.session.get('auth_response')

            if auth_response:

                timestamp = auth_response.get('expiration')
                expired = datetime.datetime.fromtimestamp(
                    timestamp) <= datetime.datetime.now()
                return not expired

            return False

        except Exception as e:
            raise AuthenticationFailed('Internal server error.')

    def authenticate_header(self, request):
        return 'CustomAuth3'
