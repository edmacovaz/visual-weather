import json
import urllib
from BeautifulSoup import BeautifulSoup

from django.conf import settings

from base.cache import cache_result
from base.models import WeatherData


WEATHER_URL = "http://api.aerisapi.com/forecasts/?limit={number_days}&p={lat},{lon}&client_id={client_id}&client_secret={client_secret}&from={when}"

def kph_to_bft(speed):
    speed_in_mps = speed / 3.6
    return int(round((speed_in_mps / .836) ** (2. / 3.)))


@cache_result()
def get_data(lat, lon, number_days=3, when="today"):

    json_data = urllib.urlopen(WEATHER_URL.format(client_id=settings.HAMWEATHER_CLIENT_ID,
                                                  client_secret=settings.HAMWEATHER_CLIENT_SECRET,
                                                  lat=lat,
                                                  lon=lon,
                                                  number_days=number_days,
                                                  when=when)).read()

    data = json.loads(json_data)
    forecasts = []
    for period in data['response'][0]['periods']:
        parsed_data = {}
        parsed_data['temp'] = period['avgTempC']
        parsed_data['mintemp'] = period['minTempC']
        parsed_data['maxtemp'] = period['maxTempC']
        parsed_data['pressure'] = period['pressureMB']
        parsed_data['precipation'] = period['precipMM']
        parsed_data['wind'] = kph_to_bft(period['windSpeedMaxKPH'])
        parsed_data['dewpoint'] = period['dewpointC']
        forecasts.append(parsed_data)
    return forecasts


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

def date_matching_weather(lat, lon, when="today"):
    return find_matches(get_data(lat, lon, when=when)[0], limit=1)[0].date

def dates_matching_current_weather(lat, lon, limit=1):
    for wd in find_matches(get_data(lat, lon, number_days=1)[0], limit=limit):
        yield wd.date


def date_matching_current_weather(lat, lon):
    return dates_matching_current_weather(lat, lon).next()


if __name__ == "__main__":
    print date_matching_current_weather(52.529531,13.411978)