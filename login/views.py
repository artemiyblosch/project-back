from django.http import JsonResponse,\
    HttpRequest, \
    HttpResponseBadRequest, \
    HttpResponseForbidden
from db.models import User

def auth(request : HttpRequest):
    u = User.strict_find(request,["tag","password"])

    if u == None: return HttpResponseBadRequest()
    if u: return JsonResponse(u[0].json())
    return HttpResponseForbidden()