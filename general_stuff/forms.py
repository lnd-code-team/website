from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields =  ['title', 'text', 'image', 'is_published']


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields =  ['title', 'text', 'image', 'is_published']


class TaglineForm(forms.ModelForm):
    class Meta:
        model = models.Tagline
        fields = ['title', 'text']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['phone_number', 'avatar', 'status', 'bio']
