from django.shortcuts import render,redirect
from django.http import request
from .models import Exercise,Workout
from .form import ExerciseForm,WorkoutForm
from .workout_templates import push_day_template


# Create your views here.
def Home(request):
    exercises = Exercise.objects.all()
    workouts = Workout.objects.all()

    context = {'exercises': exercises, 'workouts': workouts}
    return render(request,"fitness_app/home.html",context)

#workout view
def workout_view(request):
    workouts = Workout.objects.all()
    return render(request,'workouts/view_workouts.html',{'workouts':workouts})


    

#template_view
def template_request_view(request):
    push_day_template()
    # return render(request, 'fitness_app/home.html')
    return redirect('workout_view')


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
        return redirect('workout_view')
    return render(request, 'workouts/create_workout.html', {'form':form})

#delete workout routine
def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if request.method == 'POST':
        for exercise in workout.exercises.all():
            exercise.delete()
        workout.delete()
        return redirect('workout_view')
    return render(request,'workouts/delete_workout.html',{'workout':workout})

#add new exercise
#remove later (testing purposes)
def add_exercise(request):
    
    form = ExerciseForm()
    if request.method == 'POST':

        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'exercises/add_exercise.html', {'form':form})

def add_exercise_to_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    form = ExerciseForm()

    if request.method == 'POST':

        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save()

            workout.exercises.add(new_exercise)
            return redirect('workout_view')
    
    return render(request, 'exercises/add_exercise.html', {'form':form})


# update exercise
def update_exercise_view(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    form = ExerciseForm(instance=exercise)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('workout_view')  
    return render(request, 'exercises/add_exercise.html', {'form':form})


#delete exercise
def delete_exercise_view(request, exercise_id):
    exercise = Exercise.objects.get(id = exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('workout_view')
    return render(request, 'exercises/exercise_delete_view.html', {'exercise':exercise})
