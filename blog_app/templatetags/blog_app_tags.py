from django import template
from blog_app.models import Post
from django.utils import timezone

register = template.Library()


@register.simple_tag(name='list_tags')
def get_list_tags(pos, cnt_head_tag, cnt_side_tag):
    list_tags = Post.tag.most_common()
    if pos == 'head':
        return list_tags[:cnt_head_tag]
    else:
        return list_tags[cnt_head_tag:cnt_head_tag + cnt_side_tag]


@register.simple_tag(name='popular_posts')
def get_popular_posts(days, cnt_posts):
    end_date = Post.objects.last().created_at
    start_date = end_date - timezone.timedelta(days=days)
    popular_posts = Post.objects.filter(
        created_at__range=(start_date, end_date)).order_by('-views')[:cnt_posts]
    # if no publications for a long time
    if len(popular_posts) < cnt_posts:
        popular_posts = Post.objects.order_by('-views', '-created_at')[:cnt_posts]
    return popular_posts
