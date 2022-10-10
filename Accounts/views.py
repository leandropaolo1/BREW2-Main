
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from Accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from Accounts.models import AccountModel
from rest_framework import status

from Accounts.serializers import(
    CustomUserRegisterSerializer,
    CustomUserLoginSerializer,
)

from django.shortcuts import redirect


class CustomUserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            json = serializer.data
            return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomeUserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            json = serializer.data
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)