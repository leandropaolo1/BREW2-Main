from rest_framework_simplejwt.tokens import AccessToken as AccessToken1
from oauth2_provider.models import AccessToken as AccessToken2
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from Accounts.models import AccountModel
from Rooms.models import RoomsModel


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        try:
            token_key = dict(
                x.split('=')
                for x in query_string.split("&")).get('token', None)

        except Exception as e:
            token_key = None

        if token_key is None:
            scope['user'] = AnonymousUser()
            return await self.app(scope, receive, send)

        account_instance = await self.get_user(token_key)
        scope['user'] = account_instance
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            token_instance = AccessToken2.objects.filter(token=token_key)
            if token_instance.exists():
                token_instance = token_instance.first()
                return token_instance.application.user

            token_instance = AccessToken1(token_key)
            if 'id' in token_instance:
                account_instance = AccountModel.objects.filter(
                    id=token_instance['id'])
                if account_instance.exists():
                    account_instance = account_instance.first()
                    return account_instance
            return AnonymousUser()

        except Exception as e:
            return AnonymousUser()


class RoomsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        path_segments = scope.get('path', '').split('/')
        contract_uuid = path_segments[3] if len(path_segments) > 3 else None
        if not contract_uuid:
            scope['contract'] = ContractModel.objects.none()
        else:
            scope['contract'] = await self.get_contract(contract_uuid)
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_contract(self, contract_uuid):
        try:
            contract_instance = ContractModel.objects.filter(
                private_uuid=contract_uuid)
            if contract_instance.exists():
                contract_instance = contract_instance.first()
                return contract_instance
            return ContractModel.objects.none()

        except Exception as e:
            return ContractModel.objects.none()


class RouteNotFoundMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            return await self.app(scope, receive, send)
        except ValueError as e:
            if (
                "No route found for path" in str(e)
                and scope["type"] == "websocket"
            ):
                await send({"type": "websocket.close"})
            else:
                raise e


"""
class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        if client_ip not in REST_SAFE_LIST_IPS:
            return HttpResponseForbidden("Your IP address is not allowed.")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            return ip

        ip = request.META.get('REMOTE_ADDR')
        return ip


"""
