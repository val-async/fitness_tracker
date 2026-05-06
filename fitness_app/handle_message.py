from django.http import HttpResponse
from django.contrib import messages

def handle_response_message(request, message: str):
    messages.success(request, message)
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response