from django.contrib import admin
from django import forms

from app.models import Chat, Message, CHAT_TYPE_PRIVATE, validate_chat


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        data = validate_chat(cleaned_data)
        return data


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'chat_type')
    list_display_links = ('id', 'slug')
    list_filter = ('chat_type',)
    search_fields = ('id', 'slug')
    readonly_fields = ('creator',)
    form = ChatForm

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj and obj.chat_type == CHAT_TYPE_PRIVATE:
            fields = fields + ('slug', 'public')
        return fields


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender_id', 'timestamp', 'seen')
    list_display_links = ('id', 'chat')
    list_filter = ('timestamp', )
    search_fields = ('id', 'sender_id', 'text')
    readonly_fields = ('sender_id', 'chat', 'seen', 'sender')
