from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chatroom/<str:pk>', views.chatroom, name="chatroom"),

    path('create-chatroom', views.createChatRoom, name="create-chatroom"),
    path('update-chatroom/<str:pk>/', views.updateChatRoom, name="update-chatroom"),
    path('delete-chatroom/<str:pk>/', views.deleteChatRoom, name="delete-chatroom"),
    path('view-feed/', views.PostList, name='view-feed')
]
