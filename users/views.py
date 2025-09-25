from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse, Http404, HttpResponseNotAllowed
from db.models import User
import json

def info(request : HttpRequest) -> HttpResponse:
    u = User.strict_find(request,["pk"])

    if u: return JsonResponse(u[0].safe_json())
    if u == None: return HttpResponseBadRequest()
    return Http404()

def create(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)
    if User.objects.filter(tag=req["tag"]): return HttpResponseNotAllowed()

    try: u = User(**req)
    except: return HttpResponseBadRequest()
    else:
        u.save()
        return JsonResponse(u.json())
    
def groups(request : HttpRequest) -> HttpResponse:
    if not (a:=User.strict_find(request,["pk"])): 
        return HttpResponseBadRequest()

    return JsonResponse({i: g.json() for i,g in enumerate(a[0].member_in.all())})