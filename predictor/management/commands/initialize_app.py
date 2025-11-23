from django.core.management.base import BaseCommand
from predictor.models import LocationLookup, ModelMetrics

class Command(BaseCommand):
    help = 'Initialize the CO2 predictor app with default data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing CO2 Predictor App...')

        locations = [
            {'city_name': 'Delhi', 'latitude': 28.6139, 'longitude': 77.2090, 'description': 'Capital city, major industrial hub'},
            {'city_name': 'Mumbai', 'latitude': 19.0760, 'longitude': 72.8777, 'description': 'Financial capital, industrial center'},
            {'city_name': 'Kolkata', 'latitude': 22.5726, 'longitude': 88.3639, 'description': 'Eastern industrial hub'},
            {'city_name': 'Chennai', 'latitude': 13.0827, 'longitude': 80.2707, 'description': 'Southern metropolitan area'},
            {'city_name': 'Bangalore', 'latitude': 12.9716, 'longitude': 77.5946, 'description': 'IT capital, tech hub'},
            {'city_name': 'Hyderabad', 'latitude': 17.3850, 'longitude': 78.4867, 'description': 'Tech and pharmaceutical hub'},
            {'city_name': 'Pune', 'latitude': 18.5204, 'longitude': 73.8567, 'description': 'Industrial and IT center'},
            {'city_name': 'Ahmedabad', 'latitude': 23.0225, 'longitude': 72.5714, 'description': 'Industrial city in Gujarat'},
        ]

        for loc_data in locations:
            loc, created = LocationLookup.objects.get_or_create(
                city_name=loc_data['city_name'],
                defaults={
                    'latitude': loc_data['latitude'],
                    'longitude': loc_data['longitude'],
                    'country': 'India',
                    'description': loc_data['description']
                }
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'✓ {status}: {loc_data["city_name"]}'))

        metric, created = ModelMetrics.objects.get_or_create(
            model_name='XGBoost',
            defaults={
                'r2_score': 0.85,
                'rmse': 0.12,
                'mae': 0.08,
                'cv_r2_mean': 0.83,
                'cv_r2_std': 0.02,
                'total_predictions': 0
            }
        )
        status = 'Created' if created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(f'✓ {status}: Model metrics'))

        self.stdout.write(self.style.SUCCESS('✓ Initialization complete!'))