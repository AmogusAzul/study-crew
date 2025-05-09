from django.shortcuts import render, redirect

def landing_redirect_view(request):
    return redirect('core-home')