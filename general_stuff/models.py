from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserInfo(models.Model):
    user =  models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Аккаунт"
    )
    phone_number = PhoneNumberField(
        max_length=15,
        blank=True,
        null=True,
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
        upload_to='avatars', verbose_name="Аватарка"
    )
    dream_team = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'username': self.user})

    class Meta:
        verbose_name = "Доп. инфо"
        verbose_name_plural="Доп. инфо"
        ordering = ("phone_number", )


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")

    slug = models.SlugField(verbose_name="Ссылка автоматически составленная из заголовка", unique=True)

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
        return f"{self.text}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post': self.post.slug})

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("post", "author")


class Tagline(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок", default="Заголовок")
    text = models.TextField(max_length=255, verbose_name="Текст", default="Текст")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Девиз"
        verbose_name_plural = "Девиз"
