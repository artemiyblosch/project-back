from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse, Http404
from db.models import Group

def get_by_pk(request : HttpRequest) -> HttpResponse:
    g = Group.strict_find(request, ["pk"])

    if g == None: return HttpResponseBadRequest()
    if g: return JsonResponse(g[0].json())
    return Http404()