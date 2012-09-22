
import sys
from cPickle import load
import json

def generate_json(pkl):
    with open(pkl) as f:
        data = load(f)
        json_data = []
        for index, entry in enumerate(data):
            json_entry = {}
            json_entry['pk'] = index + 1
            json_entry['model'] = 'base.WeatherData'
            date = entry['date'].strftime("%Y-%m-%d")
            entry['date'] = date
            json_entry['fields'] = entry
            json_data.append(json_entry)
        with open("initial_data.json", "w") as json_file:
            json_file.write(json.dumps(json_data))

if __name__ == "__main__":
    generate_json(sys.argv[1])