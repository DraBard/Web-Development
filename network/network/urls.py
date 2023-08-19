
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("<str:username>", views.user, name="user"),
    path("toggle_follow/<int:target_user_id>/", views.toggle_follow, name='toggle_follow'),
    path("edit/", views.edit, name="edit"),
    path("like/<int:target_post_id>/", views.toggle_like, name="like")
]