from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email_confirm/', views.EmailConfirmView.as_view(), name='email_confirm'),
    path('email_confirm/<uidb64>/<token>/', views.EmailConfirmVerifyView.as_view(), name='email_confirm_verify'),
    path('email_confirm/invalid/', views.EmailConfirmInvalidView.as_view(), name='email_confirm_invalid'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', views.EditUserProfileView.as_view(), name='edit_profile')
]
