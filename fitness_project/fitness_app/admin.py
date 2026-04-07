from django.contrib import admin
from .models import Exercise,Workout,ExerciseLogs,WorkoutSession,Cardio,CardioLogs


class WorkoutAdmin(admin.ModelAdmin):
    filter_horizontal = ('exercises',)
    
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Workout,WorkoutAdmin)
admin.site.register(ExerciseLogs)
admin.site.register(Cardio)
admin.site.register(CardioLogs)



# 1. Create the inline class for ExerciseLogs
class ExerciseLogsInline(admin.TabularInline):
    model = ExerciseLogs
    extra = 0  # Prevents showing extra empty rows by default
    # Optional: make logs read-only if you don't want them edited in admin
    # readonly_fields = ('exercise', 'reps', 'weight_kg', 'created_at')

class CardioLogsInline(admin.TabularInline):
    model = CardioLogs

# 2. Register WorkoutSession with the inline
@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'date', 'duration', 'is_active','log_count')
    list_filter = ('is_active', 'date', 'user')
    inlines = [ExerciseLogsInline,CardioLogsInline]
    def log_count(self, obj):
        return obj.exercise_logs.count()
    log_count.short_description = 'Exercises Logged'

