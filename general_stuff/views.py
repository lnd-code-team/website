import re
from uuid import uuid4
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from . import forms

RUSSIAN_TO_ENGLISH = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "x",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def generate_slug(title):
    title = title.lower()

    for russian, english in RUSSIAN_TO_ENGLISH.items():
        title = title.replace(russian, english)
    
    title = '-'.join(title.split())
    title = re.sub(r'[^\w\-]', '', title)

    if models.Post.objects.filter(slug=title).exists():
        title += '-' + str(uuid4())
    return title


def logout_user(request):
    logout(request)
    messages.info(request, 'До скорой встречи :D')
    return redirect('/', permanent=True)


# Views
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

                # Fetching data from form
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                image = form.cleaned_data['image']
                is_published = form.cleaned_data['is_published']
                author = request.user
                slug = generate_slug(title)

                # Create an instance of post
                models.Post.objects.create(
                    title=title[:49], text=text, image=image, is_published=is_published, author=author, slug=slug
                )
                
                # Case success
                messages.success(request, 'Пост успешно создан!')
                return redirect('/')
            
            # Case form invalid
            messages.warning(request, 'Ошибка в передаваемых данных!')
            return render(request, 'general_stuff/post_create.html', {'form': form})
        
        # Case forbidden
        messages.warning(request, 'Воу воу воу... Куда это мы так спешим, ковбой!?')
        return render(request, 'general_stuff/post-create.html')
    

class PostUpdateView(UpdateView):
    model = models.Post
    form_class = forms.PostUpdateForm
    template_name = 'general_stuff/post_update.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Статья успешно сохранена.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            messages.warning(self.request, 'У вас нет прав на редактирование этой статьи.')

        context['success_url'] = reverse('post-detail', kwargs={'slug': self.object.slug})

        return context


def delete_post(request, slug):
    post = models.Post.objects.get(slug=slug)
    
    if post and request.user.is_authenticated and request.user.is_staff:
        post.delete()
        messages.success(request, "Пост был успешно удален.")
        return redirect('/', permanent=True)
        
    elif post and not request.user.is_staff:
        messages.warning(request, "А куда это мы лезем?)")
        return redirect("/", permanent=True)

    messages.warning(request, "Такого поста нет, удалять нечего!")
    return redirect("/", permanent=True)


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

            # Case success
            messages.success(request, f'Добро пожаловать, {user}!')
            return redirect('/', permanent=True)
        
        # Case form invalid
        messages.warning(request, "Ошибка в заполнении формы!")
        return render(request, 'registration/sign_up.html', {"form": form})
