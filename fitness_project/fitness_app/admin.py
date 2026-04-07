from django.contrib import admin
from .models import Exercise,Workout,ExerciseLogs,WorkoutSession,Cardio,CardioLogs


class WorkoutAdmin(admin.ModelAdmin):
    filter_horizontal = ('exercises',)
    
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Workout,WorkoutAdmin)


