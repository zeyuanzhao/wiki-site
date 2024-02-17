from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("add", views.add, name="add"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("edit/<str:entry>", views.edit, name="edit")
]
