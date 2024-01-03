from django.views.generic import ListView, DetailView, View, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
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
        messages.warning(request, 'Этот контент требует авторизации!')
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
        messages.warning(request, "Этот контент требует авторизации!")
        return redirect('/login')

    def post(self, request):
        pass


class PostCreateView(CreateView):
    form_class = forms.PostCreateForm

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, 'general_stuff/post_create.html', {'form': self.form_class})
        elif request.user.is_authenticated and not request.user.is_staff:
            messages.warning(request, "А ты не являешься админом, дружок :D")
            return redirect('/')
        
        messages.warning(request, "Это действие требует авторизации!")
        return redirect('/login')

    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            form = self.form_class(request.POST or None, request.FILES or None)
            if form.is_valid():
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                image = form.cleaned_data['image']
                is_published = form.cleaned_data['is_published']
                author = request.user
                slug = slugify(title)
                print(title)
                print('\n\n\nSLUG', slug, 'SLUG\n\n\n')
                
                # Create an instance of post
                models.Post.objects.create(
                    title=title, text=text, image=image, is_published=is_published, author=author, slug=slug
                )
                
                messages.success(request, 'Пост успешно создан!')
                return redirect('/')

            messages.danger(request, 'Ошибка в передаваемых данных!')
            return render(request, 'general_stuff/post_create.html', {'form': form})
        
        messages.danger(request, 'Воу воу воу... Куда это мы так спешим, ковбой!?')
        return render(request, 'general_stuff/post-create.html')


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

            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('/', permanent=True)

        return render(request, 'registration/sign_up.html', {"form": form})
