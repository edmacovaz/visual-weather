import json
import urllib
from BeautifulSoup import BeautifulSoup

from django.conf import settings

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

if __name__ == "__main__":
    print get_data(52.529531,13.411978)