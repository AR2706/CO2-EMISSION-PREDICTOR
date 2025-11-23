from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Connects to the 'prediction' app
    # We use empty string '' so it handles the home page '/'
    path('', include('predictor.urls')),
]