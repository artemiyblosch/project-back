from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def echo(request : HttpRequest):
    return JsonResponse(eval(request.body.decode("utf-8")))