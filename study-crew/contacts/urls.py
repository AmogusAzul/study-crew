from django.urls import path
from .views import friends_view, blocked_view, profile_view, befriend_view

urlpatterns = [
    path('friends/', friends_view, name='contacts-friends'),
    path('blocked/', blocked_view, name='contacts-blocked'),
    path('profile/<str:username>/', profile_view, name='contacts-profile'),
    path('befriend/<int:pk>/', befriend_view, name='contacts-befriend'),
]