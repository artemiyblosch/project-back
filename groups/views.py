from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse, Http404
from db.models import Group
import json

def get_by_pk(request : HttpRequest) -> HttpResponse:
    g = Group.strict_find(request, ["pk"])
    
    if g == None: return HttpResponseBadRequest()
    if g: return JsonResponse(g[0].json())
    return Http404()

def set_vibes(request : HttpRequest) -> HttpResponse:
    g : Group = Group.strict_find(request, ["pk"])
    req = json.loads(request.body)

    g.vibes["ct"] = req["ct"]
    g.vibes["cool"] = req["cool"]
    g.vibes["sad"] = req["sad"]
    g.update_vibe().save()

    return JsonResponse({"main_vibe": g.main_vibe})