from django.shortcuts import render
from django.http import HttpResponse

def friends_view(request):
    return HttpResponse("Friends view")
def blocked_view(request):
    return HttpResponse("Blocked view")
def profile_view(request, user_id):
    return HttpResponse(f"Profile view for user {user_id}")
# Create your views here.
