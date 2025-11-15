from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse, HttpResponseNotFound
from db.models import User, Group, Message, Sticker
import json

def text(request : HttpRequest) -> HttpResponse:
    print(request.body)
    user_q = User.strict_find(request,["pk","password"])
    if user_q == None: return HttpResponseNotFound()
    user = user_q[0]

    try:
        group = Group.objects.filter(pk = (req:=json.loads(request.body))["group_pk"])[0]
        if req["type"] != 2:
            user.text(group,req["text"],req["type"])
            return JsonResponse({})
        
        sticker = Sticker.objects.get(pk=int(req["text"]))
        group.vibes[sticker.vibe] += 1
        group.update_vibe().save()

        user.text(group, sticker.image, 2)
    except KeyError:
        return HttpResponseBadRequest()
    
    return JsonResponse({})

def get_from_group(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)
    print(req)
    try:
        g = Group.objects.filter(pk = req["group"])[0]
    except (KeyError, IndexError, ValueError):
        return HttpResponseNotFound()

    ms = Message.objects.filter(group=g)
    return JsonResponse([v.json() for i,v in enumerate(ms)],safe=False)