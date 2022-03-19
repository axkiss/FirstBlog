from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('add_post/', views.AddPostView.as_view(), name='add-post'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),

]
