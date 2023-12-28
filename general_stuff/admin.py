from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'bio', 'status')
    list_display_links = [i for i in list_display]
    search_fields = (
        'phone_number', 'bio', 'status',
        'user__username', 'user__first_name', 'user__last_name',
        'user__email'
        )


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title',
        'author',
        'time_created', 'time_updated',
        'is_published'
    )
    list_display_links = [i for i in list_display]
    search_fields = (
        'title', 'slug',
        'author__username', 'author__first_name', 'author__last_name'
    )
    prepopulated_fields = {
        'slug': ('title', )
    }


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'post' 
    )
    list_display_links = [i for i in list_display]
    search_fields = (
        'post__title', 'post__text',
        'text',
        'author__username', 'author__first_name', 'author__last_name'
    )
