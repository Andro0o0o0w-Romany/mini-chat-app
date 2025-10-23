from django.contrib import admin
from .models import Conversation, Participant, Message


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1
    readonly_fields = ['joined_at', 'last_read_at']


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['sender', 'content', 'created_at']
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_group', 'created_by', 'created_at', 'updated_at']
    list_filter = ['is_group', 'created_at']
    search_fields = ['name', 'participants__user__username']
    inlines = [ParticipantInline, MessageInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'content_preview', 'created_at']
    list_filter = ['created_at', 'is_read']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'user', 'joined_at', 'unread_count']
    list_filter = ['joined_at']
    search_fields = ['user__username', 'conversation__name']
    readonly_fields = ['joined_at']

