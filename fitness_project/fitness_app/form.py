from django import forms
from .models import Exercise,Workout

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'
        labels = {
            'exercise_name': 'exercise_name',
            'exercise_sets': 'exercise_sets'
        }

        widgets = {
            'exercise_name': forms.TextInput(attrs={'placeholder': 'add exercise'}),
            'exercise_sets': forms.NumberInput(attrs={'placeholder':' 2-4'})
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields =['split']
        lables ={
            'split': 'split'
        }

        widgets = {
            'split': forms.TextInput(attrs={'placeholder': 'e.g push_day, upper '})
        }