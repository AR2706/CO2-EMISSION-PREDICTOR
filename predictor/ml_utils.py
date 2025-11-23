import joblib
import numpy as np
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None
    _model = None
    _scaler = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        try:
            self._model = joblib.load(settings.MODEL_PATH)
            self._scaler = joblib.load(settings.SCALER_PATH)
            logger.info("✓ Models loaded successfully")
        except Exception as e:
            logger.error(f"✗ Error loading models: {e}")
            raise

    @property
    def model(self):
        if self._model is None:
            self._load_models()
        return self._model

    @property
    def scaler(self):
        if self._scaler is None:
            self._load_models()
        return self._scaler

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def extract_features(self, latitude, longitude):
        delhi = (28.6139, 77.2090)
        mumbai = (19.0760, 72.8777)
        kolkata = (22.5726, 88.3639)
        chennai = (13.0827, 80.2707)

        features = np.array([[
            latitude,
            longitude,
            latitude ** 2,
            longitude ** 2,
            latitude * longitude,
            latitude ** 3,
            longitude ** 3,
            self.calculate_distance(latitude, longitude, delhi[0], delhi[1]),
            self.calculate_distance(latitude, longitude, mumbai[0], mumbai[1]),
            self.calculate_distance(latitude, longitude, kolkata[0], kolkata[1]),
            self.calculate_distance(latitude, longitude, chennai[0], chennai[1]),
        ]])

        return features

    def predict(self, latitude, longitude, model_type='tree'):
        try:
            features = self.extract_features(latitude, longitude)

            model_name = self.model.__class__.__name__.lower()
            if any(x in model_name for x in ['ridge', 'lasso', 'svr', 'kneighbors']):
                features_scaled = self.scaler.transform(features)
                prediction = self.model.predict(features_scaled)[0]
            else:
                prediction = self.model.predict(features)[0]

            prediction = max(0, float(prediction))

            return {
                'success': True,
                'prediction': prediction,
                'latitude': latitude,
                'longitude': longitude
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def batch_predict(self, locations):
        results = []
        for loc in locations:
            try:
                lat = float(loc.get('latitude') or loc.get('lat'))
                lon = float(loc.get('longitude') or loc.get('lon'))
                prediction = self.predict(lat, lon)
                results.append(prediction)
            except (ValueError, TypeError, KeyError) as e:
                results.append({'success': False, 'error': f"Invalid location: {str(e)}"})
        return results


def get_model_manager():
    return ModelManager()