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
            email = username + '@uniandes.edu.co'
            messages.success(request, f'Account created for {username}!')
            # Save the user with the email
            form.save()
            user = form.instance
            user.email = email
            user.save()

            return redirect('info-profile')
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