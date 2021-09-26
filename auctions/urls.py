from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing_view/<int:listing_id>/", views.listing_view, name="listing_view"),
    path("create", views.create, name="create"),
    path("bid/<int:listing_id>/", views.bid, name="bid"),
    path("manage_listing/<int:listing_id>/", views.manage_listing, name="manage_listing"),
    path("toggle_watchlist/<int:listing_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("comment/<int:listing_id>/", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("listings_by_category/<int:category_id>/", views.listings_by_category, name="listings_by_category"),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
