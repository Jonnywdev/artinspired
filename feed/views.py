from django.shortcuts import render
from django.views import generic, View
from .models import Post


# class PostList(generic.ListView):

#     model = Post
#     queryset = Post.objects.order_by('-created_on')
#     template_name = 'index.html'
#     paginate_by = 9


chatrooms = [
    {'id': 1, 'name': 'How to make your first logo.'},
    {'id': 2, 'name': 'What does it take to be a good designer?'},
    {'id': 3, 'name': 'Whats the best prototype design app?'},
]


def home(request):
    context = {'chatrooms': chatrooms}
    return render(request, 'feed/index.html', context)


def chatroom(request, pk):
    return render(request, 'feed/chatroom.html')
