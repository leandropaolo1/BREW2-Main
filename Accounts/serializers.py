from rest_framework import serializers
from Accounts.models import AccountModel
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken

class CustomUserRegisterSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = AccountModel
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CustomUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    refresh = serializers.CharField(min_length=8, read_only=True)
    access = serializers.CharField(min_length=8, read_only=True)
    public_id = serializers.UUIDField(read_only = True)
    class Meta:
        model=AccountModel
        fields=['email','password','refresh','access','public_id']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email= attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Email not verified, contact admin')

        return{
            'email':user.email,
            'public_id':user.public_id,
            'refresh':str(RefreshToken.for_user(user)),
            'access':str(AccessToken.for_user(user))
        }

class CustomUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True)
    public_id = serializers.UUIDField(required = True)
    class Meta:
        model=AccountModel
        fields=['email','public_id']
        extra_kwargs = {'password': {'write_only': True}}
