from rest_framework import serializers
from .models import PredictionRecord, ModelMetrics, LocationLookup

class PredictionSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    city_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if 'latitude' not in data or 'longitude' not in data:
            raise serializers.ValidationError("Latitude and longitude are required.")
        return data


class PredictionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRecord
        fields = ['id', 'latitude', 'longitude', 'predicted_co2', 'city_name', 
                  'confidence_score', 'created_at']
        read_only_fields = ['id', 'created_at']


class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = ['model_name', 'r2_score', 'rmse', 'mae', 'cv_r2_mean', 
                  'cv_r2_std', 'total_predictions', 'last_updated']
        read_only_fields = ['last_updated']


class LocationLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationLookup
        fields = ['id', 'city_name', 'latitude', 'longitude', 'country', 
                  'description', 'avg_co2_emission']
        read_only_fields = ['id']


class BulkPredictionSerializer(serializers.Serializer):
    locations = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def validate_locations(self, data):
        if not data:
            raise serializers.ValidationError("Locations list cannot be empty.")
        if len(data) > 100:
            raise serializers.ValidationError("Maximum 100 locations allowed.")
        return data