from django.shortcuts import render,redirect,get_object_or_404
from django.http import request,HttpResponse
from ..models import Workout,Cardio,CardioLogs,WorkoutSession
from ..form import CardioForm,CardioLogsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#handle response messages , custom function
from ..handle_message import handle_response_message

@login_required
def add_cardio_to_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)

    form = CardioForm()

    context = {
        'form':form,
        'workout':workout
    }

    if request.method == 'POST':
        form = CardioForm(request.POST)
        if form.is_valid():
            new_cardio = form.save(commit=False)
            new_cardio.workout = workout
            new_cardio.save()
            return handle_response_message(request,'cardio added')
        else:
            print(form.errors)

    return render(request, 'cardio/add_cardio.html',context)

@login_required
def log_cardio(request, session_id, cardio_id):
    session = get_object_or_404(WorkoutSession, id=session_id)
    cardio = get_object_or_404(Cardio,id=cardio_id)

    form = CardioLogsForm()

    if CardioLogs.objects.filter(session=session,cardio=cardio).exists():
        return HttpResponse('<span class="text-success">✅ Already Logged</span>')
    
    print(CardioLogs.objects.all())
    if request.method == 'POST':
        form = CardioLogsForm(request.POST)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.session = session
            new_log.cardio = cardio
            new_log.save()
            return handle_response_message(request,'cardio logged')
            

    context = {
        'form':form,
        'session_id':session_id,
        'cardio':cardio,
        'session':session
    }

    return render(request, 'cardio/log_cardio.html', context)
