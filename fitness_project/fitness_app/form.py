from django import forms
from .models import Exercise,Workout,ExerciseLogs,WorkoutSession,Cardio,CardioLogs,Profile
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from datetime import timedelta

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
        fields =['split','focus']
        labels ={
            'split': 'New Routine'
        }

        widgets = {
            'split': forms.TextInput(attrs={'placeholder': 'e.g push_day, upper, morning runs '})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if user updating an existing record (not creating a new one)
        if self.instance and self.instance.pk:
            self.fields['focus'].disabled = True
            # self.fields['focus'].help_text = "Focus cannot be changed after creation."

class WorkoutTemplateForm(forms.Form):
    # pick_num = {
    #     2:2,
    #     3:3
    # }
    # desired_template = forms.ChoiceField(label='how many times a week do you want to workout',choices=pick_num) #initial=3 

    split = forms.HiddenInput()

#registration form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='confirm password')
  
    class Meta:
        model = User
        fields = ['username','password']

    field_order = ['username', 'password', 'password_confirm']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data

# class ExerciseLogsForm(forms.ModelForm):
#     class Meta:
#         model = ExerciseLogs
#         fields = ['sets','reps','weight_kg']

ExerciseLogsForm = inlineformset_factory(
    WorkoutSession,
    ExerciseLogs,
    fields=('exercise','reps','weight_kg'),
    extra=0,
    widgets={'exercise':forms.HiddenInput()}, #hidding exercise, will be manually bound in log_exercise view 'num_set':forms.HiddenInput()
    can_delete=True
)

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['duration']
        widgets = {
            'duration': forms.TextInput(attrs={
                'type': 'time',
                'step': '1', # allows seconds if you want them
                'class': 'input input-bordered w-full'
            })
        }

class CardioForm(forms.ModelForm):
    class Meta:
        model = Cardio
        fields = ['cardio_type','notes']


class CardioLogsForm(forms.ModelForm):

    hours = forms.IntegerField(min_value=0, initial=0, label="Hrs",widget=forms.NumberInput(attrs={'style': 'width: 50px;', 'placeholder': '00'}))
    minutes = forms.IntegerField(min_value=0, max_value=59, initial=0, label="Mins",widget=forms.NumberInput(attrs={'style': 'width: 50px;', 'placeholder': '00'}))
    seconds = forms.IntegerField(min_value=0, max_value=59, initial=0, label="Secs",widget=forms.NumberInput(attrs={'style': 'width: 50px;', 'placeholder': '00'}))

    class Meta:
        model = CardioLogs
        fields =['notes']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': '00:30:00'}),
        }
  
    #override save method to conver input to timedelta
    def save(self, commit = True):
        instance = super().save(commit=False)

        hrs = self.cleaned_data.get('hours',0)
        mins = self.cleaned_data.get('minutes',0)
        secs = self.cleaned_data.get('seconds',0)

        instance.duration = timedelta(hours=hrs,minutes=mins,seconds=secs)

        if commit:
            instance.save()
        return instance

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','starting_weight','target_weight','gender','height']

        widgets={
            'starting_weight':forms.TextInput(attrs={'placeholder':"Weight in kg"}),
            'target_weight':forms.TextInput(attrs={'placeholder':"Weight in kg"}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if we are updating an existing record (not creating a new one)
        if self.instance and self.instance.date_of_birth is not None:
            self.fields['date_of_birth'].disabled = True
            self.fields['starting_weight'].disabled = True
            self.fields['gender'].disabled = True


