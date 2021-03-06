"""blog_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler403 = 'blog_app.views.custom_page_http_forbidden_view'
handler404 = 'blog_app.views.custom_page_not_found_view'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),
    # Django site authentication urls (for login, logout, password management)
    path('accounts/', include('users.urls', namespace='users')),
    # WYSIWYG-editor posts
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
