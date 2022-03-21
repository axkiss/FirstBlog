from django import template
from blog_app.models import Post

register = template.Library()


@register.simple_tag(name='list_tags')
def get_main_tags(pos, cnt_head_tag, cnt_side_tag):
    list_tags = Post.tag.most_common()
    if pos == 'head':
        return list_tags[:cnt_head_tag]
    else:
        return list_tags[cnt_head_tag:cnt_head_tag + cnt_side_tag]
