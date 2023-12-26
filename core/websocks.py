from websocket import create_connection
import requests
import json


class PEN4_WEBSOCKET:
    def __init__(self, TOKEN_URL, CLIENT_ID, SECRET, URL):
        self.TOKEN_URL = TOKEN_URL
        self.CLIENT_ID = CLIENT_ID
        self.SECRET = SECRET
        self.URL = URL

        self.websocket = None
        self.message = None
        self.status = None

    def connect(self):
        access_token = self._get_token()
        if access_token:
            websocket_url = f"{self.URL}?token={access_token}"
            try:
                self.websocket = create_connection(
                    websocket_url)
                self.status = "Connected"

            except Exception as e:
                self.message = f"Connection failed: {e}"
                self.status = "Failed"

    def receive(self):
        try:
            if self.websocket:
                data = self.websocket.recv()
                self.handle_data(data)
                return data

        except Exception as e:
            self.message = f"Error receiving data: {e}"
            self.status = "Error"
            return None

    def handle_data(self, data):
        try:
            message = json.loads(data)
            print(message)

        except json.JSONDecodeError as e:
            self.message = f"JSON decode error: {e}"
            self.status = "Error"

    def send(self, data):
        try:
            if self.websocket:
                self.websocket.send(json.dumps(data))

        except Exception as e:
            self.message = f"Error sending data: {e}"
            self.status = "Error"

    def disconnect(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None

    def _get_token(self):
        try:
            response = requests.post(self.TOKEN_URL, data={
                'grant_type': 'client_credentials',
                'client_id': self.CLIENT_ID,
                'client_secret': self.SECRET})
            if response.status_code == 200:
                return response.json().get('access_token')
            self.message = "Error retrieving token."
            self.status = "Token Error"
            return None

        except Exception as e:
            self.message = f"Error retrieving token: {e}"
            self.status = "Token Error"
            return None

    def __str__(self):
        return f"WebSocketManager: {self.status} - {self.message}"


class PEN3_WEBSOCKET:
    def __init__(self, TOKEN_URL, CLIENT_ID, SECRET, URL):
        self.TOKEN_URL = TOKEN_URL
        self.CLIENT_ID = CLIENT_ID
        self.SECRET = SECRET
        self.URL = URL

        self.websocket = None
        self.message = None
        self.status = None

    def connect(self):
        access_token = self._get_token()
        if access_token:
            websocket_url = f"{self.URL}?token={access_token}"
            try:
                self.websocket = create_connection(
                    websocket_url)
                self.status = "Connected"

            except Exception as e:
                self.message = f"Connection failed: {e}"
                self.status = "Failed"

    def receive(self):
        try:
            if self.websocket:
                data = self.websocket.recv()
                self.handle_data(data)
                return data

        except Exception as e:
            self.message = f"Error receiving data: {e}"
            self.status = "Error"
            return None

    def handle_data(self, data):
        try:
            message = json.loads(data)
            print(message)

        except json.JSONDecodeError as e:
            self.message = f"JSON decode error: {e}"
            self.status = "Error"

    def send(self, data):
        try:
            if self.websocket:
                self.websocket.send(json.dumps(data))

        except Exception as e:
            self.message = f"Error sending data: {e}"
            self.status = "Error"

    def disconnect(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None

    def _get_token(self):
        try:
            response = requests.post(self.TOKEN_URL, data={
                'grant_type': 'client_credentials',
                'client_id': self.CLIENT_ID,
                'client_secret': self.SECRET})
            if response.status_code == 200:
                return response.json().get('access_token')
            self.message = "Error retrieving token."
            self.status = "Token Error"
            return None

        except Exception as e:
            self.message = f"Error retrieving token: {e}"
            self.status = "Token Error"
            return None

    def __str__(self):
        return f"WebSocketManager: {self.status} - {self.message}"



"""
from django.conf import settings
import uuid
data={'type': 'create_transaction', 'data': {'receiver_private_uuid': '7b754e79-4cd5-43cf-a5e8-2c80e7e98e60', 'sender_private_uuid': 'eef1862b-28aa-4740-a31f-daf119ada5f3', 'pos_quantity': 1, 'type': 'purchase', 'transfer': False, "transaction_private_uuid": str(uuid.uuid4())}}
settings.PEN4_WEBSOCKET
"""
