from django.contrib import admin

from app.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'chat_type')
    list_display_links = ('id', 'slug')
    list_filter = ('chat_type',)
    search_fields = ('id', 'slug')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender_id', 'timestamp', 'read')
    list_display_links = ('id', 'chat')
    list_filter = ('timestamp', )
    search_fields = ('id', 'sender_id', 'text')
