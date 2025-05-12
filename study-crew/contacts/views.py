from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from contacts.models import Contact
from student.models import Student

def friends_view(request):
    return render(request, "contacts/friends.html")
def blocked_view(request):
    return render(request, "contacts/blocked_students.html")
def profile_view(request, username):

    target_user = get_object_or_404(User, username=username)

    is_friend = target_user.contact in request.user.contact.friends.all()
    is_blocked = target_user.contact in request.user.contact.blocked_students.all()

    if is_blocked:
        messages.error(request, "You've blocked this user.")

    context = {
        'target_user': target_user,
        'is_friend': is_friend,
        'is_blocked': is_blocked,
    }

    return render(request, "contacts/profile.html", context=context)

@login_required
def befriend_view(request, pk):
    target_user = get_object_or_404(Student, pk=pk).user

    if request.user.contact in target_user.contact.blocked_students.all():
        messages.error(request, "You cannot befriend a blocked user.")
        return HttpResponse(status=403)

    if request.user.contact in target_user.contact.friends.all():
        messages.error(request, "You are already friends with this user.")
        return HttpResponse(status=403)

    request.user.contact.friends.add(target_user.contact)
    messages.success(request, f"You are now friends with {target_user.username}.")

    return redirect('contacts-profile', username=target_user.username)
