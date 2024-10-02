from django.urls import path, include
from .views import InitializeFrontDataViews
urlpatterns = [
    path('init' , InitializeFrontDataViews.as_view() , name="intialize_data")
]