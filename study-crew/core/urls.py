from django.urls import path
from .views import core_home_view

urlpatterns = [
    path('', core_home_view, name='core-home'),
]