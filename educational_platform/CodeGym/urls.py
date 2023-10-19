from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("exercises", views.exercises, name="exercises"),
    path("user", views.user, name="user"),
    path("exercises/<str:exercise_id>", views.exercise, name="exercise"),
    path("exercises/run_code/", views.run_code, name="run_code"),
    path("groups", views.groups, name="groups")
]