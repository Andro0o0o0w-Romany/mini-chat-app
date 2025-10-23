import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Participant
from .serializers import MessageSerializer

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope['user']
        
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        # Check if user is participant
        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Update user online status
        await self.update_user_status(True)
        
        await self.accept()
        
        # Notify others that user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_online': True
            }
        )
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'room_group_name'):
            # Update user online status
            await self.update_user_status(False)
            
            # Notify others that user is offline
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'is_online': False
                }
            )
            
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'message')
            
            if message_type == 'message':
                content = data.get('content', '').strip()
                if not content:
                    return
                
                # Save message to database
                message = await self.save_message(content)
                
                if message:
                    # Broadcast message to room group
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message
                        }
                    )
            
            elif message_type == 'typing':
                # Broadcast typing indicator
                is_typing = data.get('is_typing', False)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'user_id': self.user.id,
                        'username': self.user.username,
                        'is_typing': is_typing
                    }
                )
                
        except json.JSONDecodeError:
            pass
    
    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message']
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        # Don't send typing indicator to the sender
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user_id': event['user_id'],
                'username': event['username'],
                'is_typing': event['is_typing']
            }))
    
    async def user_status(self, event):
        """Send user status update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_online': event['is_online']
        }))
    
    @database_sync_to_async
    def check_participant(self):
        """Check if user is a participant in the conversation"""
        try:
            Participant.objects.get(
                conversation_id=self.conversation_id,
                user=self.user
            )
            return True
        except Participant.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, content):
        """Save message to database"""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=self.user,
                content=content
            )
            serializer = MessageSerializer(message)
            return serializer.data
        except Conversation.DoesNotExist:
            return None
    
    @database_sync_to_async
    def update_user_status(self, is_online):
        """Update user online status"""
        User.objects.filter(id=self.user.id).update(is_online=is_online)

