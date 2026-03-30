from django.shortcuts import render, redirect
from django.contrib.auth import login,get_user_model
from ..form import RegisterForm
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
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