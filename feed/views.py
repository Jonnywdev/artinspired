from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic, View
from .models import Post, ChatRoom, RoomTopic, RoomMessage
from .forms import ChatRoomForm


# chatrooms = [
#     {'id': 1, 'name': 'How to make your first logo.'},
#     {'id': 2, 'name': 'What does it take to be a good designer?'},
#     {'id': 3, 'name': 'Whats the best prototype design app?'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'feed/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'feed/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    chatrooms = ChatRoom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(roomname__icontains=q) |
        Q(roomdesc__icontains=q)
    )

    topics = RoomTopic.objects.all()
    chatroom_count = chatrooms.count()
    chatroom_messages = RoomMessage.objects.all()

    context = {'chatrooms': chatrooms, 'topics': topics,
               'chatroom_count': chatroom_count,
               'chatroom_messages': chatroom_messages}
    return render(request, 'feed/index.html', context)


def chatroom(request, pk):
    chatroom = ChatRoom.objects.get(id=pk)
    chatroom_messages = chatroom.roommessage_set.all()
    participants = chatroom.participants.all()
    if request.method == 'POST':
        roommessage = RoomMessage.objects.create(
            user=request.user,
            chatroom=chatroom,
            body=request.POST.get('body')
        )
        chatroom.participants.add(request.user)
        return redirect('chatroom', pk=chatroom.id)

    context = {'chatroom': chatroom, 'chatroom_messages': chatroom_messages, 'participants': participants}
    return render(request, 'feed/chatroom.html', context)


def createChatRoom(request):
    form = ChatRoomForm
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'feed/chatroom_form.html', context)


def updateChatRoom(request, pk):
    chatroom = ChatRoom.objects.get(id=pk)
    form = ChatRoomForm(instance=chatroom)

    if request.user != chatroom.roomhost:
        messages.error(request, 'You can not update this room')
        return redirect('home')

    if request.method == 'POST':
        form = ChatRoomForm(request.POST, instance=chatroom)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'feed/chatroom_form.html', context)


def deleteChatRoom(request, pk):
    chatroom = ChatRoom.objects.get(id=pk)

    if request.user != chatroom.roomhost:
        messages.error(request, 'You can not delete this room')
        return redirect('home')

    if request.method == 'POST':
        chatroom.delete()
        return redirect('home')
    return render(request, 'feed/delete.html', {'obj': chatroom})


def PostList(request):

    # model = Post
    # queryset = Post.objects.order_by('-created_on')
    # template_name = 'feed/feed.html'
    # paginate_by = 9
    # return render(request, 'feed/feed.html')
    model = Post
    queryset = Post.objects.order_by('-created_on')
    context = {'Post': Post}
    return render(request, 'feed/feed.html', context)


def deleteRoomMessage(request, pk):
    roommessage = RoomMessage.objects.get(id=pk)

    if request.user != roommessage.user:
        messages.error(request, 'You can not delete this message')
        return redirect('home')

    if request.method == 'POST':
        roommessage.delete()
        return redirect('home')
    return render(request, 'feed/delete.html', {'obj': roommessage})
