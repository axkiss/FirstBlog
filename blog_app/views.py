import datetime
from unidecode import unidecode

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView
from django.template.defaultfilters import slugify

from taggit.models import Tag

from blog_proj.settings import EMAIL_FEEDBACK
from .forms import AddPostForm, AddCommentForm, FeedBackForm
from .models import Post, Comment
from .services import get_results_search, get_paginate_queryset
from .utils import send_feedback


class MainListView(ListView):
    """List of posts for the main page"""
    template_name = 'blog_app/home.html'
    queryset = Post.objects.all().prefetch_related('tag').only('title', 'slug', 'image', 'created_at')
    paginate_by = 20
    context_object_name = 'posts'


class PostDetailView(View):
    """Show detail of post and comments"""
    template_name = 'blog_app/post_detail.html'
    paginate_by = 20

    def get(self, request, slug, *args, **kwargs):
        post_objects = Post.objects.select_related('author').only('title', 'description', 'slug', 'description',
                                                                  'image', 'created_at', 'edited_at', 'tag', 'views',
                                                                  'author__first_name', 'author__last_name')
        post = get_object_or_404(post_objects, slug=slug)
        post.add_one_view()
        edited = (post.edited_at - post.created_at) > datetime.timedelta(minutes=1)
        comments = post.comments.select_related('username') \
            .select_related('username__extrauserprofile') \
            .only('id', 'post_id', 'text', 'created_at',
                  'username__username', 'username__first_name', 'username__last_name',
                  'username__is_staff', 'username__groups',
                  'username__extrauserprofile__avatar')
        # Make pagination for comments
        page_obj, count_objs = get_paginate_queryset(request, comments, self.paginate_by)

        context = {
            'post': post,
            'edited': edited,
            'comment_form': AddCommentForm(),
            'comments': page_obj,
            'count_comments': count_objs,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, slug, *args, **kwargs):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, slug=slug)
            text = form.cleaned_data.get('text')
            new_comment = Comment(post=post, username=request.user, text=text)
            new_comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/') + '#comments')


class AddPostView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Show form for adding a new post on blog"""
    login_url = reverse_lazy('users:login')
    permission_required = 'blog_app.add_post'
    template_name = 'blog_app/add_post.html'
    model = Post
    form_class = AddPostForm

    def form_valid(self, form):
        form.instance.slug = slugify(unidecode(form.cleaned_data['title']))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add post'
        return context


class EditPostView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Show form for editing a post on blog"""
    login_url = reverse_lazy('users:login')
    permission_required = 'blog_app.change_post'
    template_name = 'blog_app/add_post.html'
    model = Post
    form_class = AddPostForm

    def form_valid(self, form):
        form.instance.slug = slugify(unidecode(form.cleaned_data['title']))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit post'
        return context


class SearchListView(ListView):
    """List of posts including a search query"""
    template_name = 'blog_app/search.html'
    model = Post
    paginate_by = 10
    context_object_name = 'result_posts'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        return get_results_search(self.model, search_query, posts_on_page=self.paginate_by)


class TagListView(ListView):
    """List of posts including tag"""
    template_name = 'blog_app/tag.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag).order_by('-id').prefetch_related('tag').only('title', 'slug', 'image',
                                                                                          'created_at')
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['title_tag'] = self.kwargs['slug']
        return context


class FeedBackFormView(FormView):
    """Sending feedback from the blog to EMAIL_FEEDBACK"""
    template_name = 'blog_app/feedback.html'
    form_class = FeedBackForm
    success_url = reverse_lazy('blog:feedback_success')

    def get_initial(self):
        if self.request.user.is_authenticated:
            return {'name': self.request.user.get_full_name(),
                    'email': self.request.user.email}

    def form_valid(self, form):
        send_feedback(self.request, form.cleaned_data, EMAIL_FEEDBACK)
        return super(FeedBackFormView, self).form_valid(form)


class FeedBackSuccessView(TemplateView):
    """Show the message after sending feedback"""
    template_name = 'blog_app/feedback_success.html'


class AboutUsView(TemplateView):
    """Show description of the blog """
    template_name = 'blog_app/about.html'


class TermsConditionsView(TemplateView):
    """Show the terms and conditions of the blog"""
    template_name = 'blog_app/terms_and_conditions.html'


def custom_page_http_forbidden_view(request, exception):
    """Show 403 page"""
    return render(request, "blog_app/errors/403.html", {})


def custom_page_not_found_view(request, exception):
    """Show 404 page"""
    return render(request, "blog_app/errors/404.html", {})
