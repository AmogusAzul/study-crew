from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def core_home_view(request):
    return render(request, 'core/home.html')