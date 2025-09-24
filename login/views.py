from django.http import JsonResponse,\
    HttpRequest, \
    HttpResponseBadRequest, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from db.models import User
import json

@csrf_protect
def auth(request : HttpRequest):
    req = json.loads(request.body)
    
    if "name" not in req or "password" not in req:
        return HttpResponseBadRequest()
    if (a:=User.objects.filter(**req)):
        return JsonResponse(a[0].json())
    return HttpResponseForbidden()