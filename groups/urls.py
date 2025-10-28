
from django.urls import path

from . import views

urlpatterns = [
    path("/pk", views.get_by_pk, name="get-by-pk")
]
