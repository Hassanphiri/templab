from django.urls import path
from . import views

urlpatterns = [
    path('api/readings/', views.api_readings, name='api_readings'),
    path('api/historical-readings/', views.historical_readings, name='historical_readings'),
    path('', views.index, name='index'),  # Your web interface route
]