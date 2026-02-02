from django.urls import path

from . import views

urlpatterns = [
    path("add", views.add_sticker, name="text"),
    path("get", views.get_stickers,name="get-stickers")
]
