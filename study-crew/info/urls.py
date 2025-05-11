from django.urls import path
from django.contrib.auth import views as auth_views

from .views import registration_view, profile_view


urlpatterns = [
    path('register/', registration_view, name='info-register'),
    path('login/', auth_views.LoginView.as_view(template_name='info/login.html'), name='info-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='info-logout'),
    path('profile/', profile_view, name='info-profile'),
]