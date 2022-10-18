from django.contrib import admin
from .models import ChatRoom, RoomTopic, RoomMessage
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):

    list_display = ('roomname', 'roomdesc', 'roomcreated')
    list_filter = ('roomdesc', 'roomcreated')
    search_fields = ('roomname', 'roomdesc')


admin.site.register(RoomMessage)
admin.site.register(RoomTopic)
