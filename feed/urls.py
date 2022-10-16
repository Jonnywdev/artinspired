from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('Create_Post/', views.CreatePost, name='createpost'),
    path('Your_Account/', views.AccountPage, name='account')
]
