from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.views import redirect_to_login

from .forms import ExtendedUserCreationForm, InfoUpdateForm
from student.forms import SubjectFormSet

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
    user = request.user
    student = user.student
    info = user.info

    if request.method == 'POST':
        if 'submit_info' in request.POST:
            p_form = InfoUpdateForm(request.POST, instance=info)
            s_form = SubjectFormSet(instance=student)  # not submitted
            if p_form.is_valid():
                p_form.save()
        elif 'submit_subjects' in request.POST:
            p_form = InfoUpdateForm(instance=info)  # not submitted
            s_form = SubjectFormSet(request.POST, instance=student)
            if s_form.is_valid():
                s_form.save()
                s_form = SubjectFormSet(instance=student)
    else:
        p_form = InfoUpdateForm(instance=info)
        s_form = SubjectFormSet(instance=student)

    context = {
        'p_form': p_form,
        's_form': s_form,
        'title': request.user.username,
    }
    return render(request, 'info/profile.html', context)