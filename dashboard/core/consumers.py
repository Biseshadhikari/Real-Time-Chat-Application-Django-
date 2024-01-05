# consumers.py

from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync

class AsyncDashboardConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        # print('websocket connect ', event)
        # print("channel name",self.channel_name)
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        await self.channel_layer.group_add(self.groupname,self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })
        

    async def websocket_receive(self, event):
        # print('message received from ok ', event)
        await self.channel_layer.group_send(self.groupname,{'type':'chat.message','message':event['text']})
    async def chat_message(self,event):
        print(event)
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self, event):
        print("websocket disconnect...", event)
        await self.channel_layer.group_discard(self.groupname,self.channel_name)
        raise StopConsumer()
    
class DashboardConsumer(SyncConsumer):

    def websocket_connect(self, event):
        # print('websocket connect ', event)
        # print("channel name",self.channel_name)

        async_to_sync(self.channel_layer.group_add)('programmers',self.channel_name)
        self.send({
            "type": "websocket.accept",
        })
        print(self.scope)

    def websocket_receive(self, event):
        # print('message received from ok ', event)
        async_to_sync(self.channel_layer.group_send)('programmers',{'type':'chat.message','message':event['text']})
    def chat_message(self,event):
        print(event)
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    def websocket_disconnect(self, event):
        print("websocket disconnect...", event)
        async_to_sync(self.channel_layer.group_discard)('programmers',self.channel_name)
        raise StopConsumer()
