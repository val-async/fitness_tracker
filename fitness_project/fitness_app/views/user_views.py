from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,get_user_model
from ..form import RegisterForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from ..models import WorkoutSession,Profile
from ..handle_message import handle_response_message

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('workout_view')
    return render(request,'user/register.html',{'form':form})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user = request.user)
    print('prof')
    print(profile.age)
    return render(request,'user/profile.html',{'profile':profile})

#configured Login view so i can push message
class MyLoginView(SuccessMessageMixin, LoginView):
    template_name='registration/login.html'
    success_message = 'Welcome back, %(username)s!'


@login_required
def dashboard_view(request):
    profile =get_object_or_404(Profile, user = request.user)
    
    last_two_workout_sessions = WorkoutSession.objects.filter(user = request.user,is_active=False).order_by('-date')[:2]
    
    
    # to be continued 
    # last_two_ = WorkoutSession.objects.filter(user = request.user)[1]
    # print(f"Checking Session ID: {workout_session.id}")

    # workout = workout_session.workout.split
    # print(workout)

    # session_log = workout_session.cardio_logs.first()
    # print(session_log.cardio.cardio_type)
    
    # # exercise = workout.exercise_logs.first()
    # if workout.exercise_logs.first().exists():
    #     print(workout.exercise_logs.first())
    # else:
    #     print('no exercises for this split')
    
    context = {
        "user": request.user,
        "workouts_completed": profile.workouts_completed,
        "active_streak": 5,        # Hardcoded placeholder
        'last_two_workout_sessions': last_two_workout_sessions,
        'profile':profile
    }
    return render(request, 'user/dashboard.html', context)

def Profile_update_view(request):
    profile = get_object_or_404(Profile, user = request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            handle_response_message(request,'profile updated')
            return redirect('profile')

    context = {
        'form':form
    }
    return render(request, 'user/update_profile.html',context)