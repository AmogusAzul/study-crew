from django.shortcuts import render
from django.http import HttpResponse

def registration_view(request):
    return HttpResponse("<h1>Registration Page</h1>")
    # return render(request, 'info/registration.html')
def login_view(request):
    return HttpResponse("<h1>Login Page</h1>")
    # return render(request, 'info/login.html')
def logout_view(request):
    return HttpResponse("<h1>Logout Page</h1>")
    # return render(request, 'info/logout.html')
def profile_view(request):
    return HttpResponse("<h1>Profile Page</h1>")
    # return render(request, 'info/profile.html')