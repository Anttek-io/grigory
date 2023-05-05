from django import forms
from django.contrib import admin

from app.models import Chat, Message, CHAT_TYPE_PRIVATE, validate_chat_member, ChatMember, CHAT_ROLE_ADMIN


class ChatMemberForm(forms.models.BaseInlineFormSet):
    class Meta:
        model = Chat
        fields = '__all__'

    def clean(self):
        for form in self.forms:
            validate_chat_member(form.cleaned_data, form.cleaned_data['DELETE'])


class ChatMemeberInline(admin.TabularInline):
    model = ChatMember
    extra = 0
    formset = ChatMemberForm


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'chat_type')
    list_display_links = ('id', 'slug')
    list_filter = ('chat_type',)
    search_fields = ('id', 'slug')
    readonly_fields = ('creator',)
    inlines = (ChatMemeberInline,)

    def save_model(self, request, obj, form, change):
        new_obj = not obj.pk
        if new_obj:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
        if new_obj:
            obj.members.create(user=request.user, role=CHAT_ROLE_ADMIN)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj:
            fields = fields + ('chat_type',)
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
