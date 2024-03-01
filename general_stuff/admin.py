from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'bio', 'status', 'dream_team')
    list_display_links = [i for i in list_display]
    list_filter = list_display_links
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
        'created_at', 'updated_at',
        'is_published'
    )
    list_display_links = [i for i in list_display]
    list_filter = list_display_links
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
    list_filter = list_display_links
    search_fields = (
        'post__title', 'post__text',
        'text',
        'author__username', 'author__first_name', 'author__last_name'
    )


@admin.register(models.Tagline)
class TaglineAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'text' 
    )
    list_display_links = [i for i in list_display]
    list_filter = list_display_links
    search_fields = list_display_links
