from django.shortcuts import render
from django.http import HttpResponse

def friends_view(request):
    return render(request, "contacts/friends.html")
def blocked_view(request):
    return render(request, "contacts/blocked_students.html")
def profile_view(request, user_id):
    return render(request, "contacts/profile.html")
# Create your views here.
