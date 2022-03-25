from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from .forms import AddPostForm, AddCommentForm
from .models import Post, Comment
from taggit.models import Tag
import re


# Create your views here.
class MainView(View):
    template_name = 'blog_app/home.html'
    posts_on_page = 10

    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-id')
        if len(posts) != 0:
            last_post = posts[0]
        else:
            last_post = None

        # Make pagination
        paginator = Paginator(posts[1:], self.posts_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'last_post': last_post,
            'posts': page_obj
        }
        return render(request, self.template_name, context=context)


class PostDetailView(View):
    template_name = 'blog_app/post_detail.html'
    comments_on_page = 2

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        post.add_one_view()
        comment_form = AddCommentForm()
        comments = post.comments.all()

        # Make pagination
        paginator = Paginator(comments, self.comments_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'post': post,
            'comment_form': comment_form,
            'comments': page_obj,
            'count_comments': len(comments),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, slug, *args, **kwargs):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, url=slug)
            text = form.cleaned_data.get('text')
            new_comment = Comment(post=post, username=request.user, text=text)
            new_comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/') + '#comments')


class AddPostView(View):
    template_name = 'blog_app/add_post.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.has_perm_add_post():
            form = AddPostForm()
            context = {
                'form': form
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('index')

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated and request.user.has_perm_add_post():
            title = form.cleaned_data.get('title')
            url = slugify(title)
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('image')
            tags = form.cleaned_data.get('tag')
            new_post = Post(title=title, url=url, description=description, image=image, author=request.user)
            new_post.save()
            new_post.tag.add(*tags)
            return redirect(new_post.get_url())
        context = {
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)


class SearchView(View):
    template_name = 'blog_app/search.html'
    posts_on_page = 10

    def get(self, request):
        search_query = request.GET.get('q')
        result_posts = ''
        not_found = False

        # When the page is open for the first time, the search query is empty
        if search_query:
            # Find search query in database of posts
            result_posts = Post.get_results_search(search_query, posts_on_page=self.posts_on_page)
            if not result_posts:
                not_found = True

        # Make pagination
        paginator = Paginator(result_posts, self.posts_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'result_posts': page_obj,
            'count_results': paginator.count,
            'not_found': not_found,
        }
        return render(request, template_name=self.template_name, context=context)


class AboutUsView(View):
    def get(self, request):
        return render(request, 'blog_app/about.html')


class TagView(View):
    template_name = 'blog_app/tag.html'
    posts_on_page = 10

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)

        # Make pagination
        paginator = Paginator(posts, self.posts_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'title_tag': tag,
            'posts': page_obj
        }
        return render(request, template_name=self.template_name, context=context)
