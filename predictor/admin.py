from django.contrib import admin
from .models import PredictionRecord, ModelMetrics, LocationLookup

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'latitude', 'longitude', 'predicted_co2', 'created_at']
    list_filter = ['created_at']
    search_fields = ['city_name', 'latitude', 'longitude']
    readonly_fields = ['created_at', 'ip_address']
    fieldsets = (
        ('Location', {'fields': ('latitude', 'longitude', 'city_name')}),
        ('Prediction', {'fields': ('predicted_co2', 'confidence_score')}),
        ('Metadata', {'fields': ('created_at', 'ip_address', 'user_agent')}),
    )


@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'r2_score', 'rmse', 'mae', 'last_updated']
    list_filter = ['model_name', 'last_updated']
    readonly_fields = ['created_at', 'last_updated']
    fieldsets = (
        ('Model Info', {'fields': ('model_name',)}),
        ('Performance Metrics', {'fields': ('r2_score', 'rmse', 'mae', 'cv_r2_mean', 'cv_r2_std')}),
        ('Usage', {'fields': ('total_predictions',)}),
        ('Timestamps', {'fields': ('created_at', 'last_updated')}),
    )


@admin.register(LocationLookup)
class LocationLookupAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'country', 'latitude', 'longitude', 'avg_co2_emission']
    list_filter = ['country']
    search_fields = ['city_name', 'country']
    fieldsets = (
        ('Location Info', {'fields': ('city_name', 'latitude', 'longitude', 'country')}),
        ('Details', {'fields': ('description', 'avg_co2_emission')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )