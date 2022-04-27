import datetime
import unidecode
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.template.defaultfilters import slugify
from django.core.mail import BadHeaderError
from django.views.generic import TemplateView

from blog_proj.settings import EMAIL_FEEDBACK
from .forms import AddPostForm, AddCommentForm, FeedBackForm
from .models import Post, Comment
from taggit.models import Tag

from .utils import send_feedback


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
    comments_on_page = 20

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        post.add_one_view()
        edited = (post.edited_at - post.created_at) > datetime.timedelta(minutes=1)
        comment_form = AddCommentForm()
        comments = post.comments.all()

        # Make pagination
        paginator = Paginator(comments, self.comments_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'post': post,
            'edited': edited,
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
    title = 'Add post'

    def get(self, request):
        if request.user.is_authenticated and request.user.has_perm_add_post():
            form = AddPostForm()
            context = {
                'title': self.title,
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
            'title': self.title,
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)


class EditPostView(View):
    template_name = 'blog_app/add_post.html'
    title = 'Edit post'

    def get(self, request, slug):
        if request.user.is_authenticated and request.user.has_perm_edit_post():
            post = get_object_or_404(Post, url=slug)
            form = AddPostForm(instance=post)
            context = {
                'title': self.title,
                'form': form
            }
            return render(request, template_name=self.template_name, context=context)
        return redirect('post_detail', slug=slug)

    def post(self, request, slug):
        post = get_object_or_404(Post, url=slug)
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid() and request.user.is_authenticated and request.user.has_perm_edit_post():
            post.title = form.cleaned_data.get('title')
            post.url = slugify(unidecode.unidecode(post.title))
            post.description = form.cleaned_data.get('description')
            post.image = form.cleaned_data.get('image')
            tags = form.cleaned_data.get('tag')
            if list(post.tag.names()) != tags:
                post.tag.clear()
                post.tag.add(*tags)
            post.save()
            return redirect(post.get_url())
        context = {
            'title': self.title,
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


class TagView(View):
    template_name = 'blog_app/tag.html'
    posts_on_page = 10

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag).order_by('-id')

        # Make pagination
        paginator = Paginator(posts, self.posts_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'title_tag': tag,
            'posts': page_obj
        }
        return render(request, template_name=self.template_name, context=context)


class AboutUsView(TemplateView):
    template_name = 'blog_app/about.html'


class FeedBackView(View):
    template_name = 'blog_app/feedback.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = FeedBackForm(
                initial={
                    'name': request.user.get_full_name(),
                    'email': request.user.email
                })
        else:
            form = FeedBackForm()

        context = {
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        form = FeedBackForm(request.POST)

        if form.is_valid():
            try:
                send_feedback(request, form.cleaned_data, EMAIL_FEEDBACK)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('feedback_success')

        context = {
            'form': form
        }
        return render(request, template_name=self.template_name, context=context)


class FeedBackSuccsesView(TemplateView):
    template_name = 'blog_app/feedback_success.html'


class TermsConditionsView(TemplateView):
    template_name = 'blog_app/terms_and_conditions.html'


def custom_page_not_found_view(request, exception):
    return render(request, "blog_app/errors/404.html", {})
