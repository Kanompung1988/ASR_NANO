"""Test Typhoon ASR API"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TYPHOON_KEY = os.getenv("TYPHOON_API_KEY")
TYPHOON_BASE = "https://api.opentyphoon.ai/v1"
HEADERS = {"Authorization": f"Bearer {TYPHOON_KEY}"}

print("=" * 60)
print("Testing Typhoon ASR API")
print("=" * 60)
print(f"\nAPI Key: {TYPHOON_KEY[:20]}..." if TYPHOON_KEY else "No API Key!")
print(f"Base URL: {TYPHOON_BASE}")

# Test with a simple request
print("\nTesting API endpoint...")
try:
    # Try to list models or check API status
    test_url = f"{TYPHOON_BASE}/models"
    resp = requests.get(test_url, headers=HEADERS, timeout=10)
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ API connection successful!")
        print(f"Response: {resp.json()}")
    else:
        print(f"❌ API Error: {resp.status_code}")
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")

print("\n" + "=" * 60)
print("Note: If you get 400/404 errors, the ASR endpoint might require")
print("actual audio data. The web app will test this with real audio.")
print("=" * 60)
