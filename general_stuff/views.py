from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from . import forms


# Create your views here.
class HomeListView(ListView):
    def get(self, request):
        return render(
            request,
            "general_stuff/index.html",
            {
                'title': 'Legends Neve Die',
                'posts': models.Post.objects.filter(is_published=True)
            }
        )


class PostDetailView(DetailView):
    def get(self, request, slug):
        if request.user.is_authenticated:
            post = models.Post.objects.get(slug=slug)
            return render(
                request,
                "general_stuff/post_detail.html",
                {
                    'title': slug,
                    'post': post
                }
            )
        messages.warning(request, 'Этот контент требует авторизации.')
        return redirect('/login')


class UserProfileView(View):
    def get(self, request, username):
        if request.user.is_authenticated:

            main_data = get_object_or_404(User, username=username)
            rest_data = main_data.userinfo
            
            return render(
                request,
                "general_stuff/user_profile.html",
                {
                    "title": username,
                    "main_data": main_data,
                    "rest_data": rest_data
                }
            )
        messages.warning(request, "Этот контент требует авторизации.")
        return redirect('/login')

    def post(self, request):
        pass


class PostCreateView(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, 'post_create.html')

    @method_decorator(login_required(login_url='/login'))
    def post(self, request):
        pass


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login', permanent=True)


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'Вы уже в системе!')
            return redirect('/')
        
        form = forms.RegisterForm()
        return render(request, 'registration/sign_up.html', {"form": form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Creating user info instance
            userinfo = models.UserInfo(
                user=user,
                user_id=user.id,
            )
            userinfo.save()

            messages.success(request, 'Аккаунт успешно создан')
            return redirect('/', permanent=True)

        return render(request, 'registration/sign_up.html', {"form": form})
