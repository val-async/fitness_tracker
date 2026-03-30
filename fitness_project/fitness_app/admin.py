from django.contrib import admin
from .models import Exercise,Workout

class WorkoutAdmin(admin.ModelAdmin):
    filter_horizontal = ('exercises',)
    
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Workout,WorkoutAdmin)