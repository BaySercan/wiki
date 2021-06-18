from unicodedata import name
from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wiki/", views.index, name="index"),
    path("searchEntry", views.searchEntry, name="searchEntry"),
    path("create/", views.create, name="create"),
    path("update/<str:title>", views.update, name="update"),
    path("update/", views.index, name="index"),
    path("randomEntry/", views.randomEntry, name="randomEntry")
]
