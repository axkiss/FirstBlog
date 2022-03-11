from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
]

