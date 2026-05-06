from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.Home,name='home'),
    path('workout_view', views.workout_view,name="workout_view"),
    path('create_workout',views.create_workout, name="create_workout"),
    path('edit_workout_split/<int:workout_id>/', views.edit_workout_split, name='edit_workout_split'),
    path('add_exercise/<int:workout_id>/',views.add_exercise_to_workout, name="add_exercise_to_workout" ),
    path('update_exercise/<int:exercise_id>/', views.update_exercise_view, name='update_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise_view, name='exercise_delete'),
    path('template_request', views.template_request_view,name='template_request'),
    path('delete_workout/<int:workout_id>/',views.delete_workout, name="delete_workout"),
    path('clear_all_workouts',views.clear_all_workouts,name='clear_all_workouts'),
    path('register',views.register_view,name='register'),
    path('profile/',views.profile_view,name='profile'),
    path('login',views.MyLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('log_workout/<int:workout_id>/',views.log_workout,name="log_workout"),
    path('log_exercise/<int:session_id>/<int:exercise_id>/',views.log_exercise,name="log_exercise"),
    path('add_cardio_to_workout/<int:workout_id>',views.add_cardio_to_workout,name="add_cardio_to_workout"),
    path('update_cardio/<int:cardio_id>/',views.add_cardio_to_workout,name='update_cardio'),
    path('cardio_delete/<int:cardio_id>/',views.add_cardio_to_workout,name='cardio_delete'),
    path('log_cardio/<int:session_id>/<int:cardio_id>/',views.log_cardio,name="log_cardio"),
    path('Profile_update_view',views.Profile_update_view,name="Profile_update_view")
]
