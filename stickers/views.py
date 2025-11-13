from django.http import HttpRequest, \
    HttpResponse, \
    JsonResponse
import json
from db.models import Sticker

def add_sticker(request : HttpRequest) -> HttpResponse:
    req = json.loads(request.body)
    Sticker(image = req["image"], vibe=req["vibe"])
    return JsonResponse({})