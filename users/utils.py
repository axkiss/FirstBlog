from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


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