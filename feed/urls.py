from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('chatroom/<str:pk>', views.chatroom, name="chatroom"),
    path('profile/<str:pk>/', views.usersProfile, name="userprofile"),
    path('create-chatroom', views.createChatRoom, name="create-chatroom"),
    path('update-chatroom/<str:pk>/', views.updateChatRoom, name="update-chatroom"),
    path('delete-chatroom/<str:pk>/', views.deleteChatRoom, name="delete-chatroom"),
    path('delete-roommessage/<str:pk>/', views.deleteRoomMessage, name="delete-message"),
]
handler404 = "feed.views.page_not_found_view"
