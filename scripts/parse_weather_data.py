import datetime
import os
from urllib import urlopen, urlretrieve
from BeautifulSoup import BeautifulSoup


DATA_URL = "http://www.wetter-center.de/station/daten/m{year}{month}.htm"
DATA_START = (2008, 1)
DATA_END = (2012, 9)


data_names = {0: 'date',
              4: 'temp',
              5: 'mintemp',
              6: 'maxtemp',
              10: 'pressure',
              13: 'precipation',
              15: 'wind',
              17: 'winddir',
              18: 'sunshine',
              20: 'dewpoint',
              }

def parse_date(data):
    return datetime.datetime.strptime(data, "%d.%m.%Y")

def parse_temp(data):
    return float(data[:-4].replace(",", "."))

def parse_extr_temp(data):
    return parse_temp(data[10:])

def parse_pressure(data):
    return float(data[:-4].replace(",", "."))

def parse_precipation(data):
    return float(data[:-4].replace(",", "."))

def parse_wind(data):
    return int(data.split("(")[1][:-4])

def parse_sunshine(data):
    return float(data[:-2].replace(",", "."))

    
callback_map = {0: parse_date,
                4: parse_temp,
                5: parse_extr_temp,
                6: parse_extr_temp,
                10: parse_pressure,
                13: parse_precipation,
                15: parse_wind,
                18: parse_sunshine,
                20: parse_temp,
               }

def yield_data_points():
    year, month = DATA_START

    while 1:
        yield year, str(month).zfill(2)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        if (year, month) > DATA_END:
            break


def get_data_sets():
    for year, month in yield_data_points():
        print year, month
        url = DATA_URL.format(year=year, month=month)
        data = urlretrieve(url, "{year}{month}.htm".format(year=year, month=month))
        #yield data


def yield_data_sets():
    for year, month in yield_data_points():
        print year, month
        with open("{year}{month}.htm".format(year=year, month=month)) as f:
            yield f.read()


def parse_data(data):
    dom = BeautifulSoup(data)
    data_table = dom.findAll('table')[1]
    for row in data_table.findAll('tr')[1:]:

        data_coll = {}
        for index, data_value in enumerate(row.findAll('td')):
            value = data_value.text
            if index in data_names:
                if index in callback_map:
                    value = callback_map[index](value)
                data_coll[data_names[index]] = value
        yield data_coll

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "201209.htm")):
        get_data_sets()

    all_data = []
    for data in yield_data_sets():
        for daily_data in parse_data(data):
            if daily_data:
                all_data.append(daily_data)
    print all_data