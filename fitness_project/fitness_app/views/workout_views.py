from django.shortcuts import render,redirect,get_object_or_404
from django.http import request,HttpResponse
from ..models import Exercise,Workout,ExerciseLogs,WorkoutSession,Cardio,CardioLogs,Profile
from ..form import ExerciseForm,WorkoutForm,WorkoutTemplateForm,ExerciseLogsForm,WorkoutSessionForm,CardioLogsForm
from ..workout_templates import ppl_template,ul_template
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from ..handle_message import handle_response_message
from datetime import timedelta


#view workout
@login_required
def workout_view(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request,'workouts/view_workouts.html',{'workouts':workouts})

#create new workout routine
@login_required
def create_workout(request):
    form = WorkoutForm()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            new_workout = form.save(commit=False)
            new_workout.user = request.user
            new_workout.save()
        handle_response_message(request, "workout created")
        return redirect('workout_view')
    return render(request, 'workouts/create_workout.html', {'form':form})

#update workout split name:
@login_required
def edit_workout_split(request, workout_id):
    workout = Workout.objects.get(id= workout_id)
    form = WorkoutForm(instance=workout)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance = workout)
        if form.is_valid():
            form.save()
        return handle_response_message(request, 'name updated')
    return render(request, 'workouts/partials/edit_workout.html', {'form':form,'workout':workout})

#delete workout routine
@login_required
def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if request.method == 'POST':
        for exercise in workout.exercises.all():
            exercise.delete()
        workout.delete()
        return handle_response_message(request,'workout deleted')
    return render(request,'workouts/partials/delete_workout.html',{'workout':workout})

@login_required
def clear_all_workouts(request):
    if request.method == 'POST':
        for workout in Workout.objects.all():
            for exercise in workout.exercises.all():
                exercise.delete()
            workout.delete()
        return redirect('workout_view')
    return render(request,'workouts/clear_all_workouts.html')

#template_view
@login_required
def template_request_view(request):
    print('123')
    print(request.POST)
    form = WorkoutTemplateForm()
    if request.method == 'POST':
        form = WorkoutTemplateForm(request.POST)
        if form.is_valid():
            name = request.POST.get('split',None)
            print('clickcing')
            print(name)
            if name == 'ppl':
                ppl_template(request.user)          
            elif name == 'ul':
                ul_template(request.user)
            return redirect('workout_view')
    return render(request,'workouts/request_template.html',{'form':form})


@login_required
def log_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    profile = get_object_or_404(Profile, user = request.user)

    # session = WorkoutSession.objects.filter(workout_id=workout_id,is_active=True).order_by('-date').first()
    # session = WorkoutSession.objects.filter(user=request.user, workout=workout,is_active=True).order_by('-date').first()

    # # create session
    # if not session:
    #     session,created = WorkoutSession.objects.get_or_create(
    #         user = request.user,
    #         workout = workout,
    #         duration = timedelta(0)
    #     )
        
    session = WorkoutSession.objects.filter(user=request.user, is_active=True).first()
    if session:
        # User already has an active session
        if session.workout.id != workout.id:
            # It's a different workout, prevent starting
            messages.error(request, f"You already have an active session for {session.workout.split}. Finish it first!")
            return redirect('workout_view')
        # else: same workout, resume this session
    else:
        # No active session, create a new one
        session = WorkoutSession.objects.create(
            user=request.user,
            workout=workout,
            duration=timedelta(0)
        )

    completed_ids = session.exercise_logs.values_list('exercise_id', flat=True)
    unique_completed = set(session.exercise_logs.values_list('exercise_id', flat=True))
    #forms
    log_workout_session_form = WorkoutSessionForm(instance=session)
    if request.method == 'POST':
        log_workout_session_form = WorkoutSessionForm(request.POST,instance=session)
        if log_workout_session_form.is_valid():
            completed_session = log_workout_session_form.save()
            completed_session.is_active = False
            profile.update_streak()
            completed_session.save()
            handle_response_message(request, 'congratulations, Logged')
            return redirect('workout_view')
        else:
            print(log_workout_session_form.errors)
    
    context ={'log_workout_session_form':log_workout_session_form,
            'workout':workout,
            'session_id':session.id,
            'completed_ids':completed_ids,
            'unique_completed': unique_completed}

    return render(request, 'workouts/log_workout.html', context)

