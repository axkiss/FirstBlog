from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'users'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
]

