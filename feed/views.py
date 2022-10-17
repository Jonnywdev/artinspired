from django.shortcuts import render
from django.views import generic, View
from .models import Post


class PostList(generic.ListView):

    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 9


class CreatePost():

    template_name = 'feed/createpost.html'


class AccountPage():

    template_name = 'feed/account.html'
