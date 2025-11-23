from django.urls import path
from .views import PredictCO2View, home_view, dashboard_view, about_view

urlpatterns = [
    path('api/predict/', PredictCO2View.as_view(), name='predict_co2'),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('about/', about_view, name='about'),
]