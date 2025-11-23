from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PredictionRecord(models.Model):
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate (-90 to 90)"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate (-180 to 180)"
    )
    predicted_co2 = models.FloatField(help_text="Predicted CO2 emission (kg CO2/kWh)")
    city_name = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"CO2 Prediction at ({self.latitude}, {self.longitude})"


class ModelMetrics(models.Model):
    model_name = models.CharField(max_length=100)
    r2_score = models.FloatField()
    rmse = models.FloatField()
    mae = models.FloatField()
    cv_r2_mean = models.FloatField()
    cv_r2_std = models.FloatField()
    total_predictions = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-r2_score']

    def __str__(self):
        return f"{self.model_name} - R²: {self.r2_score:.4f}"


class LocationLookup(models.Model):
    city_name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=100, default="India")
    description = models.TextField(blank=True)
    avg_co2_emission = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['city_name']

    def __str__(self):
        return f"{self.city_name}, {self.country}"