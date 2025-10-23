from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Participant, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for messages"""
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    sender_avatar = serializers.ImageField(source='sender.avatar', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'sender_username',
            'sender_name', 'sender_avatar', 'content', 'is_read',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at', 'updated_at']


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for conversation participants"""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    is_online = serializers.BooleanField(source='user.is_online', read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Participant
        fields = [
            'id', 'user_id', 'username', 'full_name', 'avatar',
            'is_online', 'joined_at', 'last_read_at', 'unread_count'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations"""
    participants = ParticipantSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    last_message = MessageSerializer(read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'name', 'is_group', 'created_by', 'created_by_username',
            'participants', 'participant_ids', 'last_message',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        from django.db.models import Count, Q
        
        participant_ids = validated_data.pop('participant_ids', [])
        created_by = validated_data.pop('created_by', None)
        
        # Get the user (from view's perform_create or from context)
        user = created_by if created_by else self.context['request'].user
        
        # Filter out the current user from participant_ids
        other_participant_ids = [pid for pid in participant_ids if pid != user.id]
        
        # Check if this is a 1-on-1 conversation (only 1 other participant)
        is_one_on_one = len(other_participant_ids) == 1 and not validated_data.get('is_group', False)
        
        if is_one_on_one:
            # Check if a conversation already exists between these two users
            other_user_id = other_participant_ids[0]
            
            # Find 1-on-1 conversations between these two users
            # Using distinct() to avoid duplicate rows from multiple filter() calls
            potential_convs = Conversation.objects.filter(
                participants__user=user,
                is_group=False
            ).filter(
                participants__user_id=other_user_id
            ).distinct()
            
            # Check each conversation to ensure it has exactly 2 participants
            for conv in potential_convs:
                if conv.participants.count() == 2:
                    # Found existing 1-on-1 conversation
                    return conv
        
        # Create conversation
        conversation = Conversation.objects.create(
            created_by=user,
            **validated_data
        )
        
        # Add creator as participant
        Participant.objects.create(conversation=conversation, user=user)
        
        # Add other participants
        for user_id in other_participant_ids:
            try:
                participant_user = User.objects.get(id=user_id)
                Participant.objects.create(
                    conversation=conversation,
                    user=participant_user
                )
            except User.DoesNotExist:
                pass
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for conversation list"""
    participants_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participants = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'name', 'is_group', 'participants_count',
            'last_message_preview', 'unread_count', 'other_participants',
            'created_at', 'updated_at'
        ]
    
    def get_participants_count(self, obj):
        return obj.participants.count()
    
    def get_last_message_preview(self, obj):
        last_msg = obj.last_message
        if last_msg:
            return {
                'id': last_msg.id,
                'sender': last_msg.sender.username,
                'content': last_msg.content[:100],
                'created_at': last_msg.created_at,
            }
        return None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        try:
            participant = obj.participants.get(user=user)
            return participant.unread_count
        except Participant.DoesNotExist:
            return 0
    
    def get_other_participants(self, obj):
        user = self.context['request'].user
        participants = obj.participants.exclude(user=user)
        return ParticipantSerializer(participants, many=True).data

