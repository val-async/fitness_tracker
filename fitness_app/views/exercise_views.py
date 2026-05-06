from django.shortcuts import render,redirect,get_object_or_404
from django.http import request,HttpResponse
from ..models import Exercise,Workout,ExerciseLogs,WorkoutSession
from ..form import ExerciseForm,ExerciseLogsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#handle response messages , custom function
from ..handle_message import handle_response_message

#add exerciese to workout
@login_required
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
@login_required
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
@login_required
def delete_exercise_view(request, exercise_id):
    exercise = Exercise.objects.get(id = exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return handle_response_message(request,"Exercise Removed")
    return render(request, 'exercises/partials/exercise_delete_view.html', {'exercise':exercise})


@login_required
def log_exercise(request,session_id, exercise_id):
    session = get_object_or_404(WorkoutSession, id=session_id)
    exercise = get_object_or_404(Exercise, id=exercise_id)

    initial_exercise_data = [{'exercise': exercise.id} for i in range(exercise.exercise_sets)]

    formset = ExerciseLogsForm(initial=initial_exercise_data)
    formset.extra= exercise.exercise_sets

    

    previous_log = ExerciseLogs.objects.filter(exercise=exercise).order_by('-created_at')[:2]

    # last_log = previous_log.first()

    

    #avoid duplicate loggin of exercises in one session
    #handling on front end now /log_workout.html, with completed_id query, but will leave this one in as well
    if ExerciseLogs.objects.filter(session=session,exercise=exercise).exists():
        return HttpResponse('<span class="text-success">✅ Already Logged</span>')
    


    if request.method == 'POST':
        # instantiate to manually link exercise object
        formset = ExerciseLogsForm(request.POST, instance=session,initial=initial_exercise_data)
        if formset.is_valid():            
            new_log = formset.save(commit=False)
            for log in new_log:
                log.exercise = exercise
                log.save()
        
            return handle_response_message(request,'success')
        else:
            print(formset.errors)

    context= {'formset':formset,
            'exercise':exercise,
            'previous_log':previous_log,
            'session_id':session_id,
            'session':session}
    return render(request, 'exercises/partials/log_exercise.html', context)

