from .models import SeoData
from django.core.cache import cache


def get_seo_data(request):
    data = cache.get('seodata')
    if data is None:
        data = SeoData.objects.first()
        cache.set('seodata', data, 60 * 60 * 24)
    return {'seodata': data}
