from django.db import models

# Create your models here.

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    exercise_sets = models.IntegerField()

    def __str__(self):
        return (f"{self.exercise_name} , sets {self.exercise_sets}")

class Workout(models.Model):
    split = models.CharField(max_length=100)
    
    exercises = models.ManyToManyField(Exercise)