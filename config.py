import os

# Set environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tanayparikh/Desktop/RADICAL AI/GeminiExplorer/Application_key.json"

# Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyDsM8QZIAUe_MW1hMftWuEm4PyzRGDQESg"

# Vertex AI settings
PROJECT_ID = "gemini-explorer-426501"
LOCATION = "us-central1"
MODEL_ENDPOINT = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/gemini-pro"
