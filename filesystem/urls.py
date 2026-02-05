
from django.urls import path

from . import views

urlpatterns = [
    path("mkdir", views.mkdir, name="make_dir"),
    path("upload", views.upload, name="make_files"),
    path("tree", views.get_tree, name="get_tree"),
    path("download", views.download, name="download")
]
