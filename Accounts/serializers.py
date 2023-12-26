from Accounts.models import AccountModel, MessageModel, CustomAccountManager
from django.contrib.auth import authenticate
from rest_framework import serializers


class AccountSerializer1(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        min_length=8)

    phone = serializers.CharField(
        max_length=255,
        min_length=8)

    password = serializers.CharField(
        max_length=255,
        min_length=8)

    email = serializers.EmailField()

    def create(self, validated_data):
        try:
            return CustomAccountManager().create_user(
                **validated_data)
        except:
            raise serializers.ValidationError()


class AccountSerializer2(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=255,
        min_length=8)


class AccountModelSerializer1(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = AccountModel
        fields = [
            'first_name',
            'last_name',
            'is_active',
            'username',
            'country',
            'joined',
            'email',
            'phone']

    def get_country(self, obj):
        try:
            return str(obj.country.name)
        except:
            return "None"


class AccountModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = [
            'is_active',
            'email',
            'id']

    def get_country(self, obj):
        try:
            return str(obj.country.name)
        except:
            return "None"


class MessagesModelSerializer1(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = MessageModel
        fields = [
            'public_uuid',
            'message',
            'header',
            'is_active',
            'is_featured',
            'date_created']

    def get_date_created(self, obj):
        return obj.date_created.strftime('%d-%m-%Y %H:%M')
