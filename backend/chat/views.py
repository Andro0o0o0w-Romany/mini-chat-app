from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Max, Prefetch
from django.utils import timezone
from .models import Conversation, Message, Participant
from .serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            participants__user=user
        ).prefetch_related(
            'participants__user',
            'messages'
        ).distinct()
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation or return existing one"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check BEFORE saving if this will be an existing conversation
        participant_ids = request.data.get('participant_ids', [])
        other_participant_ids = [pid for pid in participant_ids if pid != request.user.id]
        is_one_on_one = len(other_participant_ids) == 1 and not request.data.get('is_group', False)
        
        existing_conversation = None
        if is_one_on_one:
            other_user_id = other_participant_ids[0]
            potential_convs = Conversation.objects.filter(
                participants__user=request.user,
                is_group=False
            ).filter(
                participants__user_id=other_user_id
            ).distinct()
            
            # Check each conversation to ensure it has exactly 2 participants
            for conv in potential_convs:
                if conv.participants.count() == 2:
                    existing_conversation = conv
                    break
        
        # Save the serializer (will return existing or create new)
        self.perform_create(serializer)
        
        # Re-serialize the instance to get the latest data
        instance = serializer.instance
        output_serializer = self.get_serializer(instance)
        
        headers = self.get_success_headers(output_serializer.data)
        
        # Add a flag to indicate if this is an existing conversation
        response_data = output_serializer.data.copy()
        response_data['is_existing'] = existing_conversation is not None
        
        return Response(
            response_data,
            status=status.HTTP_200_OK if existing_conversation else status.HTTP_201_CREATED,
            headers=headers
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get conversation statistics for dashboard"""
        user = request.user
        conversations = self.get_queryset()
        
        # Total conversations
        total_conversations = conversations.count()
        
        # Total messages sent by user
        total_messages_sent = Message.objects.filter(sender=user).count()
        
        # Total unread messages
        total_unread = 0
        for conv in conversations:
            try:
                participant = conv.participants.get(user=user)
                total_unread += participant.unread_count
            except Participant.DoesNotExist:
                pass
        
        # Recent conversations (last 5)
        recent_conversations = conversations[:5]
        
        return Response({
            'total_conversations': total_conversations,
            'total_messages_sent': total_messages_sent,
            'total_unread': total_unread,
            'recent_conversations': ConversationListSerializer(
                recent_conversations,
                many=True,
                context={'request': request}
            ).data
        })
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark all messages in conversation as read"""
        conversation = self.get_object()
        try:
            participant = conversation.participants.get(user=request.user)
            participant.last_read_at = timezone.now()
            participant.save()
            return Response({'status': 'messages marked as read'})
        except Participant.DoesNotExist:
            return Response(
                {'error': 'Not a participant'},
                status=status.HTTP_403_FORBIDDEN
            )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation')
        
        queryset = Message.objects.filter(
            conversation__participants__user=user
        ).select_related('sender', 'conversation')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

