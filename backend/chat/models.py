from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Represents a conversation between users"""
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.name:
            return self.name
        participants = self.participants.all()[:2]
        return f"Conversation: {', '.join([p.user.username for p in participants])}"
    
    @property
    def last_message(self):
        return self.messages.first()
    
    def get_participants_display(self):
        """Get comma-separated list of participant usernames"""
        return ', '.join([p.user.username for p in self.participants.all()])


class Participant(models.Model):
    """Represents a user's participation in a conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversation_participants'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['conversation', 'user']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.conversation}"
    
    @property
    def unread_count(self):
        """Count unread messages for this participant"""
        return self.conversation.messages.filter(
            created_at__gt=self.last_read_at
        ).exclude(sender=self.user).count()


class Message(models.Model):
    """Represents a message in a conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

