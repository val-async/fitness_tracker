from django.shortcuts import render,redirect
from django.http import request


def Home(request):
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,"fitness_app/home.html")