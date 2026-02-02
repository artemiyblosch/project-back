from django.urls import path

from . import views

urlpatterns = [
    path("text", views.text, name="text"),
    path("gfg", views.get_from_group, name="get_messages")
]
