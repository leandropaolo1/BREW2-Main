from channels.generic.websocket import AsyncWebsocketConsumer
from Accounts.serializers import AccountModelSerializer2
from channels.db import database_sync_to_async
from Accounts.models import AccountModel
import json


class AccountsConsumer1(AsyncWebsocketConsumer):
    RATE_PERIOD = 60
    RATE_LIMIT = 10

    async def connect(self):
        if self.scope["user"] is None or self.scope["user"].is_anonymous:
            print("User is not authenticated")
            await self.close()
            return
        await self.channel_layer.group_add(
            "applications1_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "applications1_group", self.channel_name)

    async def send_data(self, event):
        await self.send(text_data=json.dumps(event['text']))

    async def receive(self, text_data=None):
        try:
            data = json.loads(text_data)
            await self.process_data(data)
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
            return

    async def account_data(self, event):
        print("PEN3 account_data", event)
        await self.send(text_data=json.dumps({
            "type": "account_data",
            "data": event['data']
        }))

    async def process_data(self, data):
        try:
            request_type = data.get("type")
            private_uuid = data['data'].get("private_uuid")
            if request_type == "account_data":
                account_data = await self.account_data_request(
                    private_uuid)
                if account_data is None:
                    await self.send_error("Invalid private_uuid")
                    return
                print("PEN3 account_data", account_data)
                await self.send_response(
                    account_data, "account_data")
            elif request_type == "test_data":
                await self.send_response("test_data")
            else:
                await self.send_error("Invalid request type")
        except Exception as e:
            await self.send_error("Invalid request type")

    async def send_response(self, message, type="account_data"):
        await self.channel_layer.group_send(
            "applications1_group", {
                'type': str(type),
                'data': message
            })

    async def send_error(self, message):
        await self.channel_layer.group_send(
            "applications1_group", {
                'type': 'response_error',
                'text': message
            })

    @database_sync_to_async
    def account_data_request(self, private_uuid):
        try:
            return AccountModelSerializer2(
                AccountModel.objects.get(id=private_uuid)
            ).data
        except AccountModel.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    @database_sync_to_async
    def get_account(self, private_uuid):
        try:
            return AccountModel.objects.get(id=private_uuid)
        except AccountModel.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    @database_sync_to_async
    def company_data_request(self, private_uuid):
        try:
            account_instance = AccountModel.objects.get(id=private_uuid)
            return AccountModelSerializer2(account_instance).data
        except AccountModel.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None