from blog_app.models import SeoData


def get_seo_data(request):
    return {'seodata': SeoData.objects.first()}
