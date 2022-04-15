from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from PIL import Image


def send_email_for_verify(request, user):
    '''
    Sending email with link for verify user email address
    :param request:
    :param user:
    :return:
    '''
    email_template_name = 'users/email_confirm_email.html',
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    context = {
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': request.scheme,
    }

    message = render_to_string(email_template_name, context=context)
    email = EmailMessage(f'Verify email - {site_name}',
                         message,
                         to=[user.email]
                         )
    email.send()


def make_square_img(height_side, img_path):
    """
    Crop to square and resize
    :param height_side:
    :param img_path:
    :return:
    """
    pic = Image.open(img_path)
    if pic.width != pic.height:
        # crop to center square
        min_side = min(pic.width, pic.height)
        if min_side == pic.height:
            start_point = int((pic.width - pic.height) // 2)
            area = (start_point, 0, start_point + pic.height, pic.height)
            pic = pic.crop(area)
        else:
            start_point = int((pic.height - pic.width) // 2)
            area = (0, start_point, pic.width, start_point + pic.width)
            pic = pic.crop(area)

    # resize
    pic.thumbnail((height_side, height_side), Image.LANCZOS)
    pic.save(img_path)
