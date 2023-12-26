from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django.contrib.auth import authenticate
from rest_framework.response import Response
from Accounts.models import AccountModel
from rest_framework.views import APIView
from rest_framework import status

from Accounts.serializers import (
    MessagesModelSerializer1,
    AccountModelSerializer1,
    AccountSerializer1,
    AccountSerializer2)


class AccountRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer1

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class AccountLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer2

    def create_token(self, validated_data):
        try:
            password = validated_data.get('password')
            email = validated_data.get("email")
            account = AccountModel.objects.get(email=email)
            account = authenticate(email=email, password=password)
            if not account:
                raise NotFound()
            refresh = RefreshToken.for_user(account)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'expiration': str(refresh.access_token.payload['exp']),
                'public_uuid': account.public_uuid,
                'private_uuid': account.id}
        except:
            raise NotFound()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            self.create_token(validated_data=serializer.validated_data),
            status=status.HTTP_200_OK)


class AccountView1(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountModelSerializer1

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        account = get_object_or_404(AccountModel, id=user.id)
        serializer = self.get_serializer(account)
        return Response(serializer.data)


class AccountView2(RetrieveAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = AccountModelSerializer1

    def retrieve(self, request, *args, **kwargs):
        private_uuid = self.request.query_params.get('private_uuid')
        if private_uuid is not None:
            account = get_object_or_404(
                AccountModel, id=private_uuid)
            serializer = self.get_serializer(account)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
