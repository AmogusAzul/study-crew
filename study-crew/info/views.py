from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.views import redirect_to_login

from .forms import ExtendedUserCreationForm

def registration_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = username + '@uniandes.edu.co'
            messages.success(request, f'Your account has been created!')
            # Save the user with the email
            form.save()
            user = form.instance
            user.email = email
            user.save()

            return redirect_to_login('info-profile')
    else:
        form = ExtendedUserCreationForm()

    return render(request, 'info/registration.html', context={
        'form': form,
    })

def logout_view(request):
    return render(request, 'info/logout.html')
@login_required
def profile_view(request):
    return render(request, 'info/profile.html')