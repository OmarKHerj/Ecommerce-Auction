from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.active_listings, name='active_listings'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    
    path("listingcategories", views.listingcategories, name='listingcategories'),
    path("bidlisting/<int:id>/", views.bidlisting, name='bidlisting'),
    path("addtolwatchlist/<int:id>/", views.addtowatchlist, name='addtowatchlist'),
    path("removefromwatchlist/<int:id>/", views.removefromwatchlist, name='removefromwatchlist'),
    path("watchlist/", views.watchlistview, name='watchlist'),
    path("addbid/<int:id>/", views.addbid, name='addbid'),
    path("closeauctions/<int:id>/", views.closeauctions, name='closeauctions'),
    path("addcomment/<int:id>/", views.addcomment, name='addcomment'),
]