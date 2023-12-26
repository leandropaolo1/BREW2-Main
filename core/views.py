from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from Accounts.models import AccountModel, CustomAccountManager
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from django.conf import settings
import requests


def handle_not_found(request, exception):
    return render(request, '404/404.html', status=404)


class CustomTokenCreationView1(TokenVerifyView):
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

    def post(self, request, *args, **kwargs):
        authentication_token = request.data.get('token', None)
        if authentication_token:
            try:
                response_data = self._make_request(authentication_token)
                if response_data:
                    private_uuid = response_data.get('private_uuid')
                    try:
                        account_instance = AccountModel.objects.get(
                            private_uuid=private_uuid)

                    except AccountModel.DoesNotExist:
                        account_instance = CustomAccountManager().createAccountInstance(
                            private_uuid=private_uuid)

                    refresh = RefreshToken.for_user(account_instance)
                    access_token = refresh.access_token

                    return Response({
                        "private_uuid": private_uuid,
                        "expiration": int(access_token['exp']),
                        "access": str(access_token),
                        "refresh": str(refresh)  # The refresh token as a string
                    })

            except Exception as e:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenVerifyView1(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        authentication_token = request.data.get('token', None)
        if authentication_token:
            try:
                access_token = AccessToken(authentication_token)
                private_uuid = access_token['private_uuid']

                return Response({
                    "private_uuid": private_uuid,
                    "expiration": access_token['exp'],
                })

            except Exception as e:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
