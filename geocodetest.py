from geocodio import GeocodioClient

client = GeocodioClient('7d7bff58c5fbdf9b5afc0c7dd59d0bddcb0d9db')
location = client.geocode('truckee')
print(location.coords)