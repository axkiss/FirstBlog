from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site

from .models import SeoData


def send_feedback(request, data, email_feedback):
    """
    Sending an email with user feedback to admin
    :param request:
    :param data:
    :param email_feedback:
    :return:
    """
    email_template_name = 'blog_app/feedback_email.html',
    seo_data = SeoData.objects.first()
    if seo_data:
        site_name = seo_data.site_name
        domain = seo_data.domain
    else:
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
    name = data['name']
    email_from = data['email']
    subject = data['subject']
    main_body = data['main_body']
    context = {
        'name': name,
        'email_from': email_from,
        'subject': subject,
        'main_body': main_body,
        'domain': domain,
        'site_name': site_name,
        'protocol': request.scheme,
    }
    message = render_to_string(email_template_name, context=context)
    email = EmailMessage(
        f'{subject} - {site_name}',
        message,
        to=[email_feedback]
    )
    try:
        email.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
