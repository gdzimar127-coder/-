import requests

API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'


def geocode(address):
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    features = json_response['response']['GeoObjectCollection']['featureMember']
    return features[0]['GeoObject'] if features else None


def coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coordinates.split()
    return float(toponym_longitude), float(toponym_lattitude)

def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coordinates.split()

    ll = ','.join([toponym_longitude, toponym_lattitude])
    envelope = toponym['boundeBy']['Envelope']

    l, b = envelope['lowerCorner'].split(" ")
    r, t = envelope['upperCorner'].split(" ")

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    span = f'{dx},{dy}'

    return ll,span