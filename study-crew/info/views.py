from django.shortcuts import render
from django.http import HttpResponse

def registration_view(request):
    return render(request, 'info/registration.html')
def login_view(request):
    return render(request, 'info/login.html')
def logout_view(request):
    return render(request, 'info/logout.html')
def profile_view(request):
    return render(request, 'info/profile.html')