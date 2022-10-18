from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class RoomTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChatRoom(models.Model):
    roomhost = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(RoomTopic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    roomname = models.CharField(max_length=200)
    roomdesc = models.TextField(null=True, blank=True)
    roomupdated = models.DateTimeField(auto_now=True)
    roomcreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-roomupdated', '-roomcreated']

    def __str__(self):
        return self.roomname


class RoomMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    body = models.TextField()
    messageupdated = models.DateTimeField(auto_now=True)
    messagecreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-messageupdated', '-messagecreated']

    def __str__(self):
        return self.body[0:50]
