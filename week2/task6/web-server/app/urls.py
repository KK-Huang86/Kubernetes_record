from django.urls import path
from django.http import JsonResponse


def index(request):
    return JsonResponse({'message': 'Hello K8s'})


urlpatterns = [
    path('', index),
]
