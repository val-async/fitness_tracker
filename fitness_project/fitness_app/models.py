from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    exercise_sets = models.IntegerField()

    def __str__(self):
        return (f"{self.exercise_name} , sets {self.exercise_sets}")

class Workout(models.Model):
    split = models.CharField(max_length=100)
    
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.split
    
class User(AbstractUser):
    height = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True,blank=True)