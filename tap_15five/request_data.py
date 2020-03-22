import requests
import json
import os

def tap_data():
    endpoint = 'https://my.15five.com/api/public/pulse'
    headers = {'Authorization': 'Bearer ' + os.environ['FIFTEENFIVE_TOKEN'] }

    has_more = True
    while has_more:
        r = requests.get(endpoint, headers=headers)
        r = r.json()

        data = r['results']

        number_datapoints = len(data)
        for each in range(0, number_datapoints):
            yield {
                "id": data[each]['id'],
                "value": data[each]['value'],
                "submit_timestamp": data[each]['create_ts']
            }

        if r['next'] == None:
            has_more = False
        else:
            endpoint = r['next']


def sample_data():
    endpoint = 'https://my.15five.com/api/public/pulse'
    headers = {'Authorization': 'Bearer ' + os.environ['FIFTEENFIVE_TOKEN'] }

    r = requests.get(endpoint, headers=headers)
    r = r.json()

    data = r['results']

    print(data[0])

# sample_data()
