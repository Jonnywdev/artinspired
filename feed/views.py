from django.shortcuts import render
from django.views import generic, View
from .models import Post, ChatRoom


# class PostList(generic.ListView):

#     model = Post
#     queryset = Post.objects.order_by('-created_on')
#     template_name = 'index.html'
#     paginate_by = 9


# chatrooms = [
#     {'id': 1, 'name': 'How to make your first logo.'},
#     {'id': 2, 'name': 'What does it take to be a good designer?'},
#     {'id': 3, 'name': 'Whats the best prototype design app?'},
# ]


def home(request):
    chatrooms = ChatRoom.objects.all()
    context = {'chatrooms': chatrooms}
    return render(request, 'feed/index.html', context)


def chatroom(request, pk):
    # chatroom = ChatRoom.objects.get(id)
    context = {'chatroom': chatroom}

    return render(request, 'feed/chatroom.html', context)


def createChatRoom(request):

    context = {}
    return render(request, 'feed/chatroom_form.html', context)
    