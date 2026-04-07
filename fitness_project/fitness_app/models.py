from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date,timedelta
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    height = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True,blank=True)


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    exercise_sets = models.IntegerField()

    def __str__(self):
        return (f"{self.exercise_name} , sets {self.exercise_sets}")



class Workout(models.Model):

    FOCUS_CHOICES=[
        ('strength/hypertrophy','strength/hypertrophy'),
        ('cardio','cardio')
    ]
    #associate user
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    split = models.CharField(max_length=100)

    focus = models.CharField(max_length=100,default='strength/hypertrophy',choices=FOCUS_CHOICES,null=True)
    
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.split
    
    def delete(self,*args, **kwargs):
        for exercise in self.exercises.all():
            exercise.delete()
        return super().delete(*args, **kwargs)

# changes
class Cardio(models.Model):
    workout = models.ForeignKey(Workout,on_delete=models.CASCADE,related_name='cardio')

    cardio_type = models.CharField(max_length=50)
    # duration = models.DurationField()
    notes = models.TextField(max_length=250, null=True,blank=True)

    
class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_sessions') #added related name here so i can count completed workouts in the profile model

    workout = models.ForeignKey(Workout,on_delete=models.CASCADE,related_name="workout_logs")
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    # calories_burned

    

class ExerciseLogs(models.Model):

    session = models.ForeignKey(WorkoutSession,on_delete=models.CASCADE, related_name='exercise_logs')

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # num_set = models.PositiveBigIntegerField()
    
    reps = models.PositiveIntegerField()

    weight_kg = models.FloatField(null=True)

    def __str__(self):
        return f'{self.exercise.exercise_name} -  - {self.reps} {self.weight_kg}'
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
class CardioLogs(models.Model):
    session = models.ForeignKey(WorkoutSession,on_delete=models.CASCADE, related_name='cardio_logs')

    cardio = models.ForeignKey(Cardio,on_delete=models.CASCADE)

    duration = models.DurationField()

    notes = models.TextField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    # get formatted duration to frontend
    def formatted_duration(self):
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'cardio session: {self.cardio.cardio_type} , duration:{self.duration}'

class Profile(models.Model):
    GENDER_CHOICES =[
        ('M','male'),
        ('F','female'),
        ('PN', 'prefer not to say')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    date_of_birth = models.DateField(null=True,blank=True)
    starting_weight = models.DecimalField(max_digits=5, decimal_places=2, 
        null=True, blank=True)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, 
        null=True, blank=True)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICES,null=True,blank=True)

    # remove nulls
    current_streak = models.PositiveIntegerField(default=0)

    last_activity_date = models.DateField(null=True)

    longest_streak = models.PositiveIntegerField(default=0)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    
    def calculate_tdee(self):
        pass

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def workouts_completed(self):
        return self.user.user_sessions.filter(is_active=False).count()
    

    
    def update_streak(self):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        if self.last_activity_date == today:
            # Already updated today, do nothing
            return
        elif self.last_activity_date == yesterday:
            # Consecutive day!
            self.current_streak += 1
        else:
            # Day was missed, reset to 1
            self.current_streak = 1
        
        
        
        #  1. Handle new users
        if not self.last_activity_date:
            self.current_streak = 1
            self.last_activity_date = timezone.now()
            self.save()
            return
        
        # Update personal record
        self.last_activity_date = timezone.now()

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.save()

    @property
    def get_current_streak(self):
        return self.current_streak

