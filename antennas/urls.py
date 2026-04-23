from django.urls import path
from . import views

app_name = 'antennas'

urlpatterns = [
    path('', views.antennas_list, name='antennas_list'),
    path('<int:id>/', views.antenna_detail, name='antenna_detail'), 
]
