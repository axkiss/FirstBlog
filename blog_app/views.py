from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from .models import Post


# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-id')
        if len(posts) != 0:
            last_post = posts[0]
        else:
            last_post = posts
        posts = posts[1:]
        content = {
            'last_post': last_post,
            'posts': posts
        }
        return render(request, 'blog_app/home.html', context=content)


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        context = {
            'post': post
        }
        return render(request, 'blog_app/post_detail.html', context=context)


class AboutUsView(View):
    def get(self, request):
        return render(request, 'blog_app/about.html')

