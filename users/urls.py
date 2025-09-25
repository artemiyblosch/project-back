from django.urls import path

from . import views

urlpatterns = [
    path("/info", views.info, name="info"),
    path("/create", views.create, name="create-user"),
    path("/groups", views.groups, name="get-groups")
]
