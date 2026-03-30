from django import forms
from .models import Exercise,Workout
from django.contrib.auth import get_user_model

User = get_user_model()

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

class WorkoutTemplateForm(forms.Form):
    pick_num = {
        2:2,
        3:3
    }
    desired_template = forms.ChoiceField(label='how many times a week do you want to workout',choices=pick_num) #initial=3 

#registration form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='confirm password')
    age = forms.FloatField(widget=forms.NumberInput)
    height = forms.FloatField()

    class Meta:
        model = User
        fields = ['username','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
