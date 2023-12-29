from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


# Create your models here.
class UserInfo(models.Model):
    user =  models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Аккаунт"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Номер телефона"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="О себе"
    )
    status = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Статус"
    )
    avatar = models.ImageField(
        blank=True, null=True,
        upload_to='avatar', verbose_name="Аватарка"
        )

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} @{self.user.username}"

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'username': self.user})

    class Meta:
        verbose_name = "Доп. инфо"
        verbose_name_plural="Доп. инфо"
        ordering = ("phone_number", )


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")

    slug = models.SlugField(verbose_name="А тут лучше не трогать", unique=True)

    text = models.TextField(verbose_name="Текст")

    image = models.ImageField(
        blank=True, null=True,
        upload_to="posts_images",
        verbose_name="Фото к посту")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Последнее редактирование"
    )

    is_published = models.BooleanField(default=False, verbose_name="Опубликовать")

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор поста"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("-created_at", "title", "author")


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Комментарий принадлежит этому посту"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )

    def __str__(self):
        return f"{self.text}"[:50]

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post': self.post.slug})

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("post", "author")
