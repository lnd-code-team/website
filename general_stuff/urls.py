from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('logout/', views.logout_user, name='logout'),
    path('users/<username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('post-update/<slug:slug>/', views.PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<slug:slug>/', views.delete_post, name='post-delete'),
]
