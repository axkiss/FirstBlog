from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import View
# from django.utils.text import slugify
from django.template.defaultfilters import slugify
from .forms import AddPostForm
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


class AddPostView(View):
    template_name = 'blog_app/add_post.html'

    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated and request.user.get_perm_add_post():
            form = AddPostForm()
            context = {
                'form': form
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('index')

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated and request.user.get_perm_add_post():
            title = form.cleaned_data.get('title')
            url = slugify(title)
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('image')
            new_post = Post(title=title, url=url, description=description, image=image, author=request.user)
            new_post.save()
            return redirect(new_post.get_url())
        context = {
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)


class AboutUsView(View):
    def get(self, request):
        return render(request, 'blog_app/about.html')
