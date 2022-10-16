from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entries"),
    path("search", views.search, name="search"),
    path("error", views.search, name="error"),
    path("create", views.create, name="create"),
    path("error_create", views.error_create, name="error_create"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]

