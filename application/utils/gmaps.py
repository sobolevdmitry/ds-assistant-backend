from assistant.settings import GMAPS_GEOCODE_API_KEY
import requests

def reverse_geocode(latitude, longitude):
    r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GMAPS_GEOCODE_API_KEY}&language=en')
    if r.ok:
        response = r.json()
        return response
    return None
