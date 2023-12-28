from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, slug):
        post = models.Post.objects.get(slug=slug)
        return render(
            request,
            "general_stuff/post_detail.html",
            {
                'title': slug,
                'post': post
            }
        )


class UserProfileView(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, username):
        pass

    @method_decorator(login_required(login_url='/login'))
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
    return redirect('login', permanent=True)


def sign_up(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return reverse('home')
    else:
        form = forms.RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})
