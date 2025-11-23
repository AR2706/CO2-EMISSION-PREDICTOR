import os
import joblib
import numpy as np
import math
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse

# --- 1. CONFIGURATION & MODEL LOADING ---
class CO2PredictionConfig:
    model = None
    scaler = None

    @classmethod
    def load_models(cls):
        if cls.model is None:
            print(f"🔍 Looking for models at: {settings.MODEL_PATH}")
            try:
                # Check if file exists before loading
                if os.path.exists(settings.MODEL_PATH):
                    cls.model = joblib.load(settings.MODEL_PATH)
                    print("✅ Model loaded successfully.")
                else:
                    print(f"❌ Model file missing at {settings.MODEL_PATH}")

                if os.path.exists(settings.SCALER_PATH):
                    cls.scaler = joblib.load(settings.SCALER_PATH)
                    print("✅ Scaler loaded successfully.")
                else:
                    print(f"⚠️ Scaler file missing at {settings.SCALER_PATH} (Might be okay if model doesn't need it)")
            except Exception as e:
                print(f"❌ Error loading models: {e}")

# Load immediately on startup
CO2PredictionConfig.load_models()

# --- 2. THE API VIEW (Math Logic) ---
class PredictCO2View(APIView):
    def post(self, request):
        try:
            data = request.data
            print(f"📩 Received Data: {data}")  # Debug print

            raw_lat = data.get('latitude')
            raw_lon = data.get('longitude')

            # 1. Check for missing values
            if raw_lat is None or raw_lon is None:
                return Response({"error": "Missing latitude or longitude"}, status=400)

            # 2. Convert to float and check for validity
            try:
                lat = float(raw_lat)
                lon = float(raw_lon)
            except ValueError:
                return Response({"error": "Coordinates must be valid numbers"}, status=400)

            # 3. Check for NaN (Not a Number) or Infinity
            if math.isnan(lat) or math.isnan(lon) or math.isinf(lat) or math.isinf(lon):
                return Response({"error": "Coordinates cannot be NaN or Infinity"}, status=400)

            # Feature Engineering
            delhi = (28.6139, 77.2090)
            mumbai = (19.0760, 72.8777)
            kolkata = (22.5726, 88.3639)
            chennai = (13.0827, 80.2707)

            def get_dist(lat1, lon1, lat2, lon2):
                return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

            # Create features explicitly as floats to prevent object-type arrays
            features = np.array([[
                lat, lon, 
                lat**2, lon**2, lat*lon, 
                lat**3, lon**3,
                get_dist(lat, lon, delhi[0], delhi[1]),
                get_dist(lat, lon, mumbai[0], mumbai[1]),
                get_dist(lat, lon, kolkata[0], kolkata[1]),
                get_dist(lat, lon, chennai[0], chennai[1])
            ]], dtype=np.float64)

            # Final check for NaNs in the calculated features
            if np.isnan(features).any():
                return Response({"error": "Calculation resulted in NaN. Check inputs."}, status=400)

            model = CO2PredictionConfig.model
            scaler = CO2PredictionConfig.scaler
            
            if model is None:
                return Response({"error": "Model not loaded on server"}, status=500)

            model_type = type(model).__name__

            # Check if scaling is needed
            if model_type in ['KNeighborsRegressor', 'Ridge', 'SVR']:
                if scaler is None:
                     return Response({"error": "Scaler is required but not loaded"}, status=500)
                final_input = scaler.transform(features)
            else:
                final_input = features

            prediction = model.predict(final_input)[0]

            # Ensure prediction is a standard python float
            result_value = float(prediction)

            return Response({
                "latitude": lat,
                "longitude": lon,
                "predicted_co2_emission": round(result_value, 4),
                "units": "kg CO2/kWh",
                "model_used": model_type
            })

        except Exception as e:
            print(f"❌ Server Error: {str(e)}")
            return Response({"error": f"Internal Error: {str(e)}"}, status=400)

# --- 3. THE HTML VIEWS ---
def home_view(request):
    # This renders your Dark Mode UI
    return render(request, 'home.html')

def dashboard_view(request):
    # Returns simple text to prevent crashing (since dashboard.html is deleted)
    return HttpResponse("Dashboard Coming Soon!")

def about_view(request):
    # Returns simple text to prevent crashing (since about.html is deleted)
    return HttpResponse("About Page Coming Soon!")