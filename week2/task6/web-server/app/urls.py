import os
import redis
from django.urls import path
from django.http import JsonResponse


def index(request):
    return JsonResponse({'message': 'Hello K8s'})


def redis_test(request):
    r = redis.Redis(
        host=os.environ.get('REDIS_HOST'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        password=os.environ.get('REDIS_PASSWORD'),
        decode_responses=True,
    )
    r.set('hello', 'from-web-server')
    value = r.get('hello')
    return JsonResponse({'redis_host': os.environ.get('REDIS_HOST'), 'value': value})


urlpatterns = [
    path('', index),
    path('redis/', redis_test),
]
