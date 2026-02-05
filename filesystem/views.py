from django.http import HttpRequest, \
    HttpResponse, HttpResponseBadRequest, \
    JsonResponse, Http404, FileResponse
import json,os,pathlib
from db.models import User
from shutil import copyfileobj

def mkdir(request):
    req = json.loads(request.body)
    u = User.strict_find(request,['pk','password'])
    if u == None: return HttpResponseBadRequest()

    path = pathlib.Path(f'/home/ubuntu/users/{req['group_pk']}/{req['directory']}')
    os.mkdir(path)

def upload(request):
    req = json.loads(request.body)
    u = User.strict_find(request,['pk','password'])
    if u == None: return HttpResponseBadRequest()

    path = pathlib.Path(f'/home/ubuntu/users/{req['group_pk']}/{req['path']}')
    with open(path,'w') as f:
        copyfileobj(req['file'],f)

def download(request):
    req = json.loads(request.body)
    u = User.strict_find(request,['pk','password'])
    if u == None: return HttpResponseBadRequest()

    path = pathlib.Path(f'/home/ubuntu/users/{req['group_pk']}/{req['path']}')
    return FileResponse(open(path,'rb'))

def directory_tree(path : pathlib.Path):
    tree = [[],{}]
    for x in path.iterdir():
        if x.is_file():
            tree[0].append(x.name)
        else:
            tree[1][x.name] = directory_tree(x)
    return tree

def get_tree(request):
    req = json.loads(request.body)
    u = User.strict_find(request,['pk','password'])
    if u == None: return HttpResponseBadRequest()

    path = pathlib.Path(f'/home/ubuntu/users/{req['group_pk']}')

    return JsonResponse(directory_tree(path),safe=False)