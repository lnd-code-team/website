from django.urls import path
from . import views


urlpatterns = [
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('logout/', views.logout_user, name='logout'),
    path('users/<username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/<username>/update', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('post-update/<slug:slug>/', views.PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<slug:slug>/confirm/', views.confirm_post_delition, name='post-delete-confirm'),
    path('post-delete/<slug:slug>/<int:confirm>', views.delete_post, name='post-delete'),
    path('tagline/', views.TaglineView.as_view(), name='tagline'),
    path('about/', views.about, name='about'),
    path('', views.HomeView.as_view(), name="home"),
]
