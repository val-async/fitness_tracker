from .models import Exercise,Workout
import random
from .exercise_list import chest_workouts,shoulder_workouts,tricep_workouts,back_workouts,bicep_workouts,leg_workouts,ab_workouts
#templates
# if 4 - ul ul, fb core fb cardio 
# if 2 ul
# if 3 ppl, ul core/, ul cardio
# if 5, ppl r ul, ul core/accessories/ul, ul cardio ul
# if 6 

#workout template

# def push_day_template():
#     push_workout = Workout(split='push day')
#     push_workout.save()

#     bench_press = Exercise(exercise_name= 'bench press', exercise_sets=random.randint(1,4))
#     ohp = Exercise(exercise_name='over head press', exercise_sets = random.randint(1,4) )

#     bench_press.save()
#     ohp.save()

#     push_workout.exercises.set([bench_press,ohp,])

#apparently random.sample exists LOL
# def pick_workouts(workout_list: list, num: int):
#     picked_list = []
#     while len(picked_list) < num:
#         work_out = random.choice(workout_list)
#         if work_out not in picked_list:
#             picked_list.append(work_out)
#         else:
#             continue
#     return picked_list


def add_exercies_to_workout_split(workout_list : list, workout_split: Workout):
    for work_out in workout_list:
        new_exercise = Exercise(exercise_name=work_out[0], exercise_sets=work_out[1])
        new_exercise.save()
        workout_split.exercises.add(new_exercise)

def ppl_template():
    #pick push exercises and add to workout model
    push_workout = Workout(split='push day')
    push_workout.save()

    picked_chest_workouts = random.sample(chest_workouts,3)
    picked_shoulder_workouts = random.sample(shoulder_workouts,2)
    picked_tricep_workouts = random.sample(tricep_workouts,2)

    
    picked_push_workouts = picked_chest_workouts + picked_shoulder_workouts + picked_tricep_workouts

    add_exercies_to_workout_split(picked_push_workouts,push_workout)

    #pick pull exercise and add to workout model
    pull_workout = Workout(split='pull day')
    pull_workout.save()

    picked_back_workouts = random.sample(back_workouts, 4)
    picked_bicep_workouts = random.sample(bicep_workouts,2)

    picked_pull_workouts = picked_back_workouts + picked_bicep_workouts
    add_exercies_to_workout_split(picked_pull_workouts,pull_workout)

    #pick leg and ab exercises
    leg_day = Workout(split="leg day")
    leg_day.save()

    picked_legs_and_abs_workout = random.sample(leg_workouts,3) + random.sample(ab_workouts,1) + [('calf raises',3)]
    add_exercies_to_workout_split(picked_legs_and_abs_workout,leg_day)
    


def ul_template():
    upper_day = Workout(split='upper')
    upper_day.save()

    picked_upper_day_workouts = random.sample(chest_workouts,2) + random.sample(shoulder_workouts,2)+ random.sample(bicep_workouts,1) + random.sample(back_workouts,2) + random.sample(tricep_workouts,1)

    add_exercies_to_workout_split(picked_upper_day_workouts,upper_day)

    #pick lower day workouts

    lower_day = Workout(split='lower')
    lower_day.save()

    picked_lower_day_workouts = random.sample(leg_workouts,4) + random.sample(ab_workouts,2)  + [('calf raises',3)]
    add_exercies_to_workout_split(picked_lower_day_workouts,lower_day)