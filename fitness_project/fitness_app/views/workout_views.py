from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from ..models import Exercise,Workout
from ..form import ExerciseForm,WorkoutForm,WorkoutTemplateForm
from ..workout_templates import ppl_template,ul_template
from django.contrib import messages

#handle response messages
def handle_response_message(request, message: str):
    messages.success(request, message)
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response

#view workout
def workout_view(request):
    workouts = Workout.objects.all()
    return render(request,'workouts/view_workouts.html',{'workouts':workouts})

#template_view
def template_request_view(request):
    form = WorkoutTemplateForm()
    if request.method == 'POST':
        form = WorkoutTemplateForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['desired_template']
            if num == '3':
                ppl_template()          
            elif num == '2':
                ul_template()   
            return redirect('workout_view')
    return render(request,'workouts/request_template.html',{'form':form})


#create new workout routine
def create_workout(request):
    form = WorkoutForm()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('workout_view')
    return render(request, 'workouts/create_workout.html', {'form':form})

#update workout split name:
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
def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if request.method == 'POST':
        for exercise in workout.exercises.all():
            exercise.delete()
        workout.delete()
        return handle_response_message(request,'workout deleted')
    return render(request,'workouts/partials/delete_workout.html',{'workout':workout})

def clear_all_workouts(request):
    if request.method == 'POST':
        for workout in Workout.objects.all():
            for exercise in workout.exercises.all():
                exercise.delete()
            workout.delete()
        return redirect('workout_view')
    return render(request,'workouts/clear_all_workouts.html')
