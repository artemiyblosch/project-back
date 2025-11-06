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
    print("O"*1000000)
    g : Group = Group.strict_find(request, ["pk"])[0]
    if g == None: return HttpResponseBadRequest()

    try:
        req = json.loads(request.body)

        g.vibes["ct"] = int(req["ct"])
        g.vibes["cool"] = int(req["cool"])
        g.vibes["sad"] = int(req["sad"])
        g.update_vibe().save()
    except KeyError:
        return HttpResponseBadRequest()

    return JsonResponse({"main_vibe": g.main_vibe})