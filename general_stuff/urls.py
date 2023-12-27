from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name="home"),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('users/<username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create')
]

