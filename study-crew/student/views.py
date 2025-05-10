from django.shortcuts import render
from django.http import HttpResponse

def search_view(request):
    return render(request, 'student/search.html')
# Create your views here.   
