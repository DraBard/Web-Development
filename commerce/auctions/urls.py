from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_pk>", views.auction, name="listing"),
    path("bid/<int:listing_pk>", views.bid, name="bid"),
    path("watchlist/<int:listing_pk>", views.watchlist_add, name="watchlist_add"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("watchlist_delete/<int:watchlist_pk>", views.watchlist_delete, name="watchlist_delete"),
    path("close/<int:listing_pk>", views.close, name="close")
]
