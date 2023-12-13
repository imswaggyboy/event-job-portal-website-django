from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import ChatGroup
from jobs.models import *

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connection Established...')
        user = self.scope['user']
        # print('Current user is ..', user)
        # print('Channel layer is...',self.channel_layer)
        # print('Channel name is...',self.channel_name)
        self.groupname = self.scope['url_route']['kwargs']['jobGroupId']
        print('Group name is...',self.groupname)
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()

    async def get_job_id(self,id):
        return await database_sync_to_async(Jobs.objects.get)(id=int(id))
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            # job = database_sync_to_async(Jobs.objects.get)(id=int(self.groupname))
            job = await self.get_job_id(self.groupname)
            print('Job is....',job) 
            chat = ChatGroup(content=text_data,job=job,member=self.scope['user'])
            await database_sync_to_async(chat.save)()


            # print('Message received from client....', text_data)
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type':'chat_message',
                    'message':text_data
                }
            )
        else:
            print('received empty message...')
        

    async def chat_message(self,event):
        await self.send(text_data = event['message'])
        print(event['message'])


    async def disconnect(self, close_code):
        print("Connection Disconnected....",close_code)
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        raise StopConsumer()