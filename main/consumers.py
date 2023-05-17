from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import Group
import json
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.group_id = self.scope["url_route"]["kwargs"].get("group_id")
		await self.accept()
		chat_messages = await self.get_chat_messages()
		await self.channel_layer.group_add(
			self.group_id, self.channel_name)
		await self.send(json.dumps({
			"type": "group_messages",
			"messages": chat_messages
		}))
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(self.group_id, self.channel_name)
	
	async def receive(self, text_data):
		message = json.loads(text_data).get("message", "")
		chat_messages = await self.create_message(message)
		
		await self.channel_layer.group_send(
			self.group_id, {"type": "broadcast_message", "messages": chat_messages})
	
	@database_sync_to_async
	def create_message(self, message):
		group = Group.objects.get(id=self.group_id)
		group.message_set.create(
			sender=self.scope["user"],
			message=message
		)
	
	@database_sync_to_async
	def get_chat_messages(self):
		group = Group.objects.get(id=self.group_id)
		messages = list(group.message_set.all().values())
		
		for message in messages:
			message["group_id"] = str(message["group_id"])
			message["time_created"] = str(message["time_created"])
			message["sender"] = User.objects.get(id=message["sender_id"]).username
		
		return messages
		
	async def broadcast_message(self, event):
		chat_messages = await self.get_chat_messages()
		await self.send(json.dumps({
			"type": "group_messages",
			"messages": chat_messages
		}))

