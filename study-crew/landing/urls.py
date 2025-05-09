from django.urls import path
from .views import landing_redirect_view

urlpatterns = [
    path('', landing_redirect_view, name='landing'),
]