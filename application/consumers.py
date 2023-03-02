import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from personnel.models import Staff
from asgiref.sync import async_to_sync


class IncomeCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        await self.channel_layer.group_add(str(user_id), self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        await self.channel_layer.group_discard(str(user_id), self.channel_name)

    async def send_income_call(self, event):
        if 'number_in' in event:
            number_in = event['number_in']
        else:
            number_in = ''
        if 'end_time' in event:
            end_time = event['end_time']
            print(end_time)
        else:
            end_time = ''
        await self.send(json.dumps({
            'end_time': end_time,
            'number_in': number_in,
            'count_call_new_appeal': event['count_call_new_appeal'],
            'data_for_number_in': event['data_for_number_in'],
            'unique_id': event['unique_id'],
            'api': event['api']
        }))



class Statistic(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('statistic', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('statistic', self.channel_name)

    async def send_statics_call_number(self, event):
        # print('OPERATORS IN CONSUMERS OF WEBSOCKET', event)
        await self.send(json.dumps({
            'operators': event['operators']
        }))

    async def send_statics_question_category(self, event):
        # print('OPERATORS IN CONSUMERS OF WEBSOCKET', event)
        await self.send(json.dumps({
            'question_category': event['question_category']
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user_id = self.scope['user']
        self.room_group_name = str(user_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message2 = text_data_json['message2']
        latitude_temp = text_data_json['latitude_temp']
        longitude_temp = text_data_json['longitude_temp']
        print('recive-message:', message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message2': message2,
                'latitude_temp': latitude_temp,
                'longitude_temp': longitude_temp,
            }
        )

    def chat_message(self, event):
        message = event['message']
        message2 = event['message2']
        latitude_temp = event['latitude_temp']
        longitude_temp = event['longitude_temp']
        print('chat')
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'message2': message2,
            'latitude_temp': latitude_temp,
            'longitude_temp': longitude_temp,

        }))


