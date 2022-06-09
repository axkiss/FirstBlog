from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.MainListView.as_view(), name='index'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('feedback/', views.FeedBackFormView.as_view(), name='feedback'),
    path('feedback/success/', views.FeedBackSuccessView.as_view(), name='feedback_success'),
    path('terms_conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('tag/<slug:slug>', views.TagListView.as_view(), name='tag')
]