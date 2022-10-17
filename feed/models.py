from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Post(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_image")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    favourite = models.ManyToManyField(User, related_name='post_faves', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    body = models.TextField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class RoomTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChatRoom(models.Model):
    roomhost = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(RoomTopic, on_delete=models.SET_NULL, null=True)
    # peoplejoined =
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

    def __str__(self):
        return self.body[0:50]
