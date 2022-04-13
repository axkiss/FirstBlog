from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('feedback/', views.FeedBackView.as_view(), name='feedback'),
    path('feedback/succses/', views.FeedBackSuccsesView.as_view(), name='feedback_success'),
    path('terms_conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('tag/<slug:slug>', views.TagView.as_view(), name='tag')
]