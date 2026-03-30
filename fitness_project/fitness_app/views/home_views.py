from django.shortcuts import render,redirect
from django.http import request
from ..models import Exercise,Workout
from ..form import ExerciseForm,WorkoutForm

def Home(request):
    exercises = Exercise.objects.all()
    workouts = Workout.objects.all()

    context = {'exercises': exercises, 'workouts': workouts}
    return render(request,"fitness_app/home.html",context)