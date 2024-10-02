
from django.urls import path, include
from .views import (AddFavoritesView , RemoveFavoriteView)

urlpatterns = [
    path("favorites/add" , AddFavoritesView.as_view() , name="addToFavorite"),
    path("favorites/remove" , AddFavoritesView.as_view() , name="removeFavorite")
]