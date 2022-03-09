from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about', views.AboutUsView.as_view(), name='about'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
]
