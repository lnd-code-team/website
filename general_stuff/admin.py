from django.contrib import admin
import django.contrib.auth.models as admin_models
from . import models


# Register your models here.
@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username',
        'first_name', 'last_name',
        'email', 'phone_number',
        'is_staff'
    )
    list_display_links = [i for i in list_display]
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'bio')


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


admin.site.unregister(admin_models.User)
admin.site.unregister(admin_models.Group)

