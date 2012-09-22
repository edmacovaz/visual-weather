import json
import urllib
from BeautifulSoup import BeautifulSoup

from django.conf import settings

from base.models import WeatherData

WEATHER_URL = "http://api.aerisapi.com/forecasts/?limit=1&p={lat},{lon}&client_id={client_id}&client_secret={client_secret}"

def kph_to_bft(speed):
    speed_in_mps = speed / 3.6
    return int(round((speed_in_mps / .836) ** (2. / 3.)))


def get_data(lat, lon):
    
    json_data = urllib.urlopen(WEATHER_URL.format(client_id=settings.HAMWEATHER_CLIENT_ID,
                                                  client_secret=settings.HAMWEATHER_CLIENT_SECRET,
                                                  lat=lat,
                                                  lon=lon)).read()

    data = json.loads(json_data)
    real_data = data['response'][0]['periods'][0]
    parsed_data = {}
    parsed_data['temp'] = real_data['avgTempC']
    parsed_data['mintemp'] = real_data['minTempC']
    parsed_data['maxtemp'] = real_data['maxTempC']
    parsed_data['pressure'] = real_data['pressureMB']
    parsed_data['precipation'] = real_data['precipMM']
    parsed_data['wind'] = kph_to_bft(real_data['windSpeedMaxKPH'])
    parsed_data['dewpoint'] = real_data['dewpointC']
    return parsed_data


def find_matches(data, limit=5):

        scores = {}
        for inst in WeatherData.objects.all():
            score = 0
            for key, value in data.items():
                data_value = getattr(inst, key)
                diff = (value - data_value)**2
                score += diff
            scores[inst.id] = score ** (1./2)
        pks = [pk for pk, score in sorted(scores.items(), key=lambda x: x[1])[:limit]]
        return WeatherData.objects.filter(pk__in=pks).all()


def dates_matching_current_weather(lat, lon, limit=1):
    for wd in find_matches(get_data(lat, lon), limit=limit):
        yield wd.date


def date_matching_current_weather(lat, lon):
    return dates_matching_current_weather(lat, lon).next()


if __name__ == "__main__":
    print date_matching_current_weather(52.529531,13.411978)