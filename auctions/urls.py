from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("product_add", views.product_add, name="product_add"),
    path("product_category", views.product_category, name="product_category"),
    path("product_my", views.product_my, name="product_my"),
    path("product_comment", views.product_comment, name="product_comment"),
    path("product/<str:title>/<int:id>", views.product_detail, name="product_detail"),
    path("product_watchlist", views.product_watchlist, name="product_watchlist"),
    path("product_watchlist_add/<int:id>", views.product_watchlist_add, name="product_watchlist_add"),
    path("product_watchlist_remove/<int:id>", views.product_watchlist_remove, name="product_watchlist_remove"),
    path("product_bid/<int:productid>/<int:amount>", views.product_bid, name="product_product_bid"),
    path("product_close/<int:productid>", views.product_close, name="product_product_close")
]
