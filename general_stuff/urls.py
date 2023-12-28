from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name="home"),
    path('logout/', views.logout_user, name='logout'),
    path('user/<username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
]
