import requests


def find_coors_by_text(query: str) -> tuple:
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': query, 'format': 'json'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]['lat'], data[0]['lon']
        raise AttributeError('No coordinates found for query: ' + query)
    raise RuntimeError('Failed to get coordinates for query: ' + query + 'status code: ' + str(response.status_code))