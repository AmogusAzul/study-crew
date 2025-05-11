from django.urls import path
from .views import registration_view, login_view, logout_view, profile_view

urlpatterns = [
    path('register/', registration_view, name='info-register'),
    path('login/', login_view, name='info-login'),
    path('logout/', logout_view, name='info-logout'),
    path('profile/', profile_view, name='info-profile'),
]