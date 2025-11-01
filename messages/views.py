from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse#, HttpResponseNotFound
from db.models import User, Group, Message
import json

def text(request : HttpRequest) -> HttpResponse:
    print(request.body)
    user_q = User.strict_find(request,["pk","password"])
    if user_q == None: return JsonResponse({}) #BUG
    user = user_q[0]

    try:
        group = Group.objects.filter(pk = (req:=json.loads(request.body))["group_pk"])[0]
        match req['vibes']:
            case 0: group.vibe_ct += 1
            case 1: group.vibe_cl += 1
            case 2: group.vibe_sd += 1
        
        user.text(group,req["text"],req["type"])
        return JsonResponse({})
    except KeyError:
        return HttpResponseBadRequest()

def get_from_group(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)
    print(req)
    try:
        g = Group.objects.filter(pk = req["group"])[0]
    except (KeyError, IndexError, ValueError):
        return JsonResponse({})#BUG

    ms = Message.objects.filter(group=g)
    return JsonResponse([v.json() for i,v in enumerate(ms)],safe=False)