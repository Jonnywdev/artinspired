from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic, View
from .models import ChatRoom, RoomTopic, RoomMessage
from .forms import ChatRoomForm


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


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
    chatroom_messages = RoomMessage.objects.filter(Q(chatroom__topic__name__icontains=q))

    context = {'chatrooms': chatrooms, 'topics': topics,
               'chatroom_count': chatroom_count,
               'chatroom_messages': chatroom_messages}
    return render(request, 'feed/index.html', context)


def usersProfile(request, pk):
    user = User.objects.get(id=pk)
    chatrooms = user.chatroom_set.all()
    chatroom_messages = user.roommessage_set.all()
    topics = RoomTopic.objects.all()
    context = {"user": user, "chatrooms": chatrooms, 'chatroom_messages': chatroom_messages, 'topics': topics}
    return render(request, 'feed/profile.html', context)


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


@login_required(login_url='login')
def createChatRoom(request):
    form = ChatRoomForm()

    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)
            chatroom.roomhost = request.user
            chatroom.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'feed/chatroom_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteChatRoom(request, pk):
    chatroom = ChatRoom.objects.get(id=pk)

    if request.user != chatroom.roomhost:
        messages.error(request, 'You can not delete this room')
        return redirect('home')

    if request.method == 'POST':
        chatroom.delete()
        return redirect('home')
    return render(request, 'feed/delete.html', {'obj': chatroom})


def deleteRoomMessage(request, pk):
    roommessage = RoomMessage.objects.get(id=pk)

    if request.user != roommessage.user:
        messages.error(request, 'You can not delete this message')
        return redirect('home')

    if request.method == 'POST':
        roommessage.delete()
        return redirect('home')
    return render(request, 'feed/delete.html', {'obj': roommessage})


@login_required(login_url='login')
def updateprofile(request):
    return render(request, 'feed/update-profile.html')
