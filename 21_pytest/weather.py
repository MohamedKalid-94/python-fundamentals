import json
import urllib.request


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read())


def current_temp(city):
    data = fetch_json(f"https://api.example.com/weather?city={city}")
    return round(data["main"]["temp"] - 273.15, 1)