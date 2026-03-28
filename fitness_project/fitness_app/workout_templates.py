from .models import Exercise,Workout

#workout template
def push_day_template():
    push_workout = Workout(split='push day')

    bench_press = Exercise(exercise_name= 'bench press', exercise_sets=3)
    ohp = Exercise(exercise_name='over head press', exercise_sets = 3 )

    bench_press.save()
    ohp.save()
    push_workout.save()

    push_workout.exercises.set([bench_press,ohp])