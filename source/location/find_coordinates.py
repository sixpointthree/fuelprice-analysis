import requests


def find_coors_by_text(query: str) -> tuple:
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': query, 'format': 'json'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        raise AttributeError(f'No coordinates found for query len({len(query)}): {query}')
    raise RuntimeError(f'Failed to get coordinates for query: {query}, status_code: {response.status_code}')