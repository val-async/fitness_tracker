from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('workout_view', views.workout_view,name="workout_view"),
    path('create_workout',views.create_workout, name="create_workout"),
    path('edit_workout_split/<int:workout_id>/', views.edit_workout_split, name='edit_workout_split'),
    path('add_exercise',views.add_exercise, name="add_exercise" ),
    path('add_exercise/<int:workout_id>/',views.add_exercise_to_workout, name="add_exercise_to_workout" ),
    path('update_exercise/<int:exercise_id>/', views.update_exercise_view, name='update_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise_view, name='exercise_delete'),
    path('template_request', views.template_request_view,name='template_request'),
    path('delete_workout/<int:workout_id>/',views.delete_workout, name="delete_workout")
]
