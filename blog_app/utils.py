from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from blog_app.models import SeoData


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
    site_name = seo_data.site_name
    domain = seo_data.domain
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
    email.send()
