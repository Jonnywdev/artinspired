from django.contrib import admin
from .models import Post, Comment, ChatRoom, RoomTopic, RoomMessage
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'created_on')
    list_display = ('title', 'slug', 'created_on')
    search_fields = ('title', 'content')
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('body', 'created_on')
    search_fields = ('name', 'body')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):

    list_display = ('roomname', 'roomdesc', 'roomcreated')
    list_filter = ('roomdesc', 'roomcreated')
    search_fields = ('roomname', 'roomdesc')


admin.site.register(RoomMessage)
admin.site.register(RoomTopic)
