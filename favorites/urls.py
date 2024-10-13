
from django.urls import path, include
from .views import (AddFavoritesView)

urlpatterns = [
    path("favorites" , AddFavoritesView.as_view() , name="addToFavorite")
]