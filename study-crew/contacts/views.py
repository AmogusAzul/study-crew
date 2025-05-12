from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse

def friends_view(request):
    return render(request, "contacts/friends.html")
def blocked_view(request):
    return render(request, "contacts/blocked_students.html")
def profile_view(request, username):

    target_user = get_object_or_404(User, username=username)

    is_friend = target_user in request.user.contact.friends.all()
    is_blocked = target_user in request.user.contact.blocked_students.all()

    if is_blocked:
        messages.error(request, "You've blocked this user.")

    context = {
        'target_user': target_user,
        'is_friend': is_friend,
        'is_blocked': is_blocked,
    }

    return render(request, "contacts/profile.html", context=context)
# Create your views here.
