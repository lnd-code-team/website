from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from . import models


# Create your views here.
class HomeListView(ListView):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "general_stuff/index.html",
            {
                'title': 'Legends Neve Die',
                'posts': models.Post.objects.filter(is_published=True)
            }
        )


class PostDetailView(DetailView):
    def get(self, request, slug, *args, **kwargs):
        post = models.Post.objects.get(slug=slug)

        return render(
            request,
            "general_stuff/detail.html",
            {
                'title': slug,
                'post': post
            }
        )


class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        pass

    def post(self, request):
        pass


class PostCreateView(View):
    def get(self, request):
        return render(request, 'post_create.html')

    def post(self, request):
        pass

