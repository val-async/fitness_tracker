from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from ..form import RegisterForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,password=password)
            login(request,user)
            return redirect('workout_view')
    return render(request,'user/register.html',{'form':form})

@login_required
def profile_view(request):
    return render(request,'user/profile.html')