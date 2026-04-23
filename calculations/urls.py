from django.urls import path
from .views import antenna_calculate

urlpatterns = [
    path("antenna/calculate/", antenna_calculate, name="antenna_calculate"),
]
