import re
from uuid import uuid4
from django.views.generic import DetailView, View, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from . import models
from . import forms

# FIRST OF ALL
#
# run './manage.py makemigrations general_stuff'
# './manage.py migrate'
# then in admin.py create first TAGLINE
# then u can create userinfo instance for your admin user

FORBIDDEN = "У вас недостаточно прав для открытия данного ресурса."
AUTHORIZATION_REQUIRED = "Этот контент требует авторизации."
FORM_INVALID = "Ошибка в передаваемых данных."
NO_URL = "Ресурс не существует!"

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
    return redirect('/login', permanent=True)


def about(request):
    return render(
        request,
        'general_stuff/about.html'
    )


def confirm_post_delition(request, slug):
    try:
        post = get_object_or_404(models.Post, slug=slug)
        return render(request, 'general_stuff/confirm_post_delition.html', {'post': post})
    except Exception:
        messages.warning(request, NO_URL)
        return redirect('home')


def delete_post(request, slug, confirm):
    if not confirm:
        messages.warning(request, FORM_INVALID)
        return redirect('home')

    if request.user.is_staff:
        try:
            post = models.Post.objects.get(slug=slug)
        except Exception:
            messages.warning(request, NO_URL)
            return redirect('/', permanent=True)

        post.delete()
        messages.success(request, "Пост был успешно удален.")
        return redirect('/posts', permanent=True)

    # case forbidden
    messages.warning(request, FORBIDDEN)
    return redirect("/", permanent=True)


# Views
class HomeView(View):
    def get(self, request, **kwargs):
        search_term = request.GET.get('q')

        if search_term:
            query = Q(title__icontains=search_term) | Q(text__icontains=search_term)
            posts = models.Post.objects.filter(query)

            end_is_one = str(len(posts))[-1] == '1'
            end_is_lesser_five = str(len(posts))[-1] in ('2', '3' ,'4')

            if end_is_one:
                messages.info(request, f"Найден {len(posts)} пост!")
            elif end_is_lesser_five:
                messages.info(request, f"Найдено {len(posts)} поста!")
            else:
                messages.info(request, f"Найдено {len(posts)} постов!")

                if str(len(posts)) == '0':
                    return redirect('/')

            return render(request, 'general_stuff/posts.html', {'posts': posts, 'search_term': search_term})

        # case just home view
        return render(
            request,
            "general_stuff/index.html",
            {
                'posts': models.Post.objects.filter(is_published=True),
                'tagline': models.Tagline.objects.all()[0],
                'dreamteam': models.UserInfo.objects.filter(dream_team=True),
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
                    'post': post,
                    'tagline': models.Tagline.objects.all()[0],
                    'dreamteam': models.UserInfo.objects.filter(dream_team=True),
                }
            )
        
        # case unauthorized
        messages.warning(request, AUTHORIZATION_REQUIRED)
        return redirect('/login')


class PostCreateView(CreateView):
    form_class = forms.PostCreateForm

    def get(self, request):
        if request.user.is_staff:
            return render(request, 'general_stuff/post_create.html', {'form': self.form_class})

        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/')

    def post(self, request):
        if request.user.is_staff:

            form = self.form_class(request.POST or None, request.FILES or None)
            if form.is_valid():

                # fetching data from request
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                image = form.cleaned_data['image']
                is_published = form.cleaned_data['is_published']
                author = request.user
                slug = generate_slug(title)

                # create an instance of post
                models.Post.objects.create(
                    title=title[:49], text=text, image=image, is_published=is_published, author=author, slug=slug
                )
                
                messages.success(request, 'Пост успешно создан!')
                return redirect('/')
            
            # case form invalid
            messages.warning(request, FORM_INVALID)
            return render(request, 'general_stuff/post_create.html', {'form': form})
        
        # case forbidden
        messages.warning(request, FORBIDDEN)
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
        return reverse(
            'post-detail',
            kwargs={
                'slug': self.object.slug
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            messages.warning(self.request, FORBIDDEN)

        context['success_url'] = reverse(
            'post-detail',
            kwargs={
                'slug': self.object.slug
            }
        )

        return context


class PostListView(View):
    def get(self, request):
        if request.user.is_staff:
            posts = models.Post.objects.all()
            return render(
                request,
                "general_stuff/posts.html",
                {
                    "posts": posts,
                    'tagline': models.Tagline.objects.all()[0],
                    'dreamteam': models.UserInfo.objects.filter(dream_team=True),
                }
            )

        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/', permanent=True)


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
        
        # case unauthorized
        messages.warning(request, AUTHORIZATION_REQUIRED)
        return redirect('/login')


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'Вы уже в системе!')
            return redirect('/')

        form = forms.RegisterForm()
        return render(request, 'registration/sign_up.html', {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            form = forms.RegisterForm(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user)

                # creating userinfo instance
                userinfo = models.UserInfo(
                    user=user,
                    user_id=user.id,
                )
                userinfo.save()

                # case success
                messages.success(request, f'Добро пожаловать, {user}!')
                return redirect('/', permanent=True)
            
            # case form invalid
            messages.warning(request, FORM_INVALID)
            return render(request, 'registration/sign_up.html', {"form": form})


class TaglineView(View):
    form_class = forms.TaglineForm
    model_class = models.Tagline

    def get(self, request):
        if request.user.is_staff:
            try:
                tagline = self.model_class.objects.all()[0]
                return render(request, 'general_stuff/tagline.html', {'form': self.form_class(instance=tagline)})
            except Exception:
                return render(request, 'general_stuff/tagline.html', {'form': self.form_class})

        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/')

    def post(self, request):
        if request.user.is_staff:
            form = self.form_class(request.POST or None)

            if form.is_valid():
                
                try:
                    # fetching data from request
                    new_title = form.cleaned_data['title']
                    new_text = form.cleaned_data['text']
                    
                    tagline = self.model_class.objects.all()[0]

                    # saving new data
                    tagline.title = new_title
                    tagline.text = new_text

                    # finishing touches                
                    tagline.save()
                except Exception:
                    self.model_class.objects.create(title=new_title, text=new_text)

                messages.success(request, "Да здравствует новое слово!")
                return redirect('/')

            # case form invalid
            tagline = self.model_class.objects.all()[0]
            messages.warning(request, FORM_INVALID)
            return render(request, 'general_stuff/tagline.html', {'form': self.form_class(instance=tagline)})

        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/')


class UserProfileUpdateView(View):
    def get(self, request, username):
        if request.user.username == username:
            user = get_object_or_404(User, username=username)
            
            user_form = forms.UserUpdateForm(instance=user)
            userinfo_form = forms.UserInfoUpdateForm(instance=user.userinfo)
            
            return render(request, 'general_stuff/user_profile_update.html', {
                'user_form': user_form,
                'userinfo_form': userinfo_form,
                'username': username
            })
        
        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/')

    def post(self, request, username):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=username)
            user_form = forms.UserUpdateForm(request.POST, instance=user)
            userinfo_form = forms.UserInfoUpdateForm(request.POST, instance=user.userinfo)
            
            if user_form.is_valid() and userinfo_form.is_valid():
                user_form.save()

                avatar = request.FILES.get('avatar')
                if avatar:
                    userinfo_form.instance.avatar = avatar

                userinfo_form.save()

                # case success
                messages.success(request, 'Профиль успешно изменен.')
                return redirect(f'/users/{username}/')
            
            # case form invalid
            messages.warning(request, FORM_INVALID)
            return render(request, 'general_stuff/user_profile_update.html', {
                'user_form': user_form,
                'userinfo_form': userinfo_form,
                'username': username
            })

        # case forbidden
        messages.warning(request, FORBIDDEN)
        return redirect('/login/')
