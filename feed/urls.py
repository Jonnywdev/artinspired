from django.urls import path
from . import views

urlpatterns = [
    # path('', views.PostList.as_view(), name='home'),
    path('', views.home, name="home"),
    path('chatroom/<str:pk>', views.chatroom, name="chatroom"),

    path('create-room', views.createChatRoom, name="create-chatroom")
]
