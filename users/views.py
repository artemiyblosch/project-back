from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from db.models import User
import json

def info(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)
    
    if "name" not in req:
        return HttpResponseBadRequest()
    if (a:=User.objects.filter(**req)):
        return JsonResponse(a[0].safe_json())
    return Http404()

def create(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)

    try: u = User(**req)
    except: return HttpResponseBadRequest()
    else:
        u.save()
        return JsonResponse()