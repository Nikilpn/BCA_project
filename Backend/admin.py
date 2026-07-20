from django.contrib import admin
from Backend.models import (
    roomtypedb, roomnamedb, staffdb,
    ChatbotResponse, ChatbotConversation, Notification
)

# Register your models here.

@admin.register(roomtypedb)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('ROOMTYPE', 'DESCRIPTION')
    search_fields = ('ROOMTYPE',)

@admin.register(roomnamedb)
class RoomNameAdmin(admin.ModelAdmin):
    list_display = ('ROOMNAME', 'ROOMTYPE', 'ROOMPRICE')
    search_fields = ('ROOMNAME',)
    list_filter = ('ROOMTYPE',)

@admin.register(staffdb)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('STAFFNAME', 'STAFFDESIGNATION')
    search_fields = ('STAFFNAME',)

@admin.register(ChatbotResponse)
class ChatbotResponseAdmin(admin.ModelAdmin):
    list_display = ('query_type', 'keyword', 'is_active', 'created_at')
    list_filter = ('query_type', 'is_active')
    search_fields = ('keyword', 'response')
    list_editable = ('is_active',)

@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = ('username', 'query_type', 'rating', 'created_at')
    list_filter = ('query_type', 'rating', 'created_at')
    search_fields = ('username', 'user_message', 'bot_response')
    readonly_fields = ('created_at', 'user_message', 'bot_response')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('username', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('username', 'title', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
