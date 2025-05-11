from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import ExtendedUserCreationForm

def registration_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            
            form.save()
            return redirect(request, 'info-profile')
    else:
        form = ExtendedUserCreationForm()

    return render(request, 'info/registration.html', context={
        'form': form,
    })
def login_view(request):
    return render(request, 'info/login.html')
def logout_view(request):
    return render(request, 'info/logout.html')
@login_required
def profile_view(request):
    return render(request, 'info/profile.html')