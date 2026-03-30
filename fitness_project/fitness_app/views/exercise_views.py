from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from ..models import Exercise,Workout
from ..form import ExerciseForm
from django.contrib import messages

#add new exercise
#remove later (testing purposes)

#handle response messages
def handle_response_message(request, message: str):
    messages.success(request, message)
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response


def add_exercise_to_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    form = ExerciseForm()

    if request.method == 'POST':

        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save()

            workout.exercises.add(new_exercise)
            return handle_response_message(request,'Exercise added')
    
    return render(request, 'exercises/partials/add_exercise.html', {'form':form,'workout': workout})


# update exercise
def update_exercise_view(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    form = ExerciseForm(instance=exercise)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return handle_response_message(request, " workout updated") 
    return render(request, 'exercises/partials/update_exercise.html', {'form':form,'exercise':exercise})


#delete exercise
def delete_exercise_view(request, exercise_id):
    exercise = Exercise.objects.get(id = exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return handle_response_message(request,"Exercise Removed")
    return render(request, 'exercises/partials/exercise_delete_view.html', {'exercise':exercise})
