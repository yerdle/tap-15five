import requests
import json
import os
import singer
from singer import utils, metadata

LOGGER = singer.get_logger()

def tap_data(config, input_stream_id, columns):
        #stream id should be plural of entity (e.g. answer entity --> answers stream)
        #drop final s to get entity path from stream id

    token = config['access_token']
    stream_path = input_stream_id[:-1]
    endpoint = 'https://my.15five.com/api/public/' + stream_path
    headers = {'Authorization': 'Bearer ' + token }

    total_records = 0
    list_endpoint = endpoint

    has_more = True
    while has_more:
                #pull list of all objects
        r_list = requests.get(list_endpoint, headers=headers)
        r_list = r_list.json()

        data = r_list['results']
            # for each item in list, pull full object
            # todo - limit based on what has already synced
        number_datapoints = len(data)
        for each in range(0, number_datapoints):
            get_endpoint = endpoint + '/' + str(data[each]['id'])
            r_get = requests.get(get_endpoint, headers=headers)
            r_get = r_get.json()

            # get only columns specified by catalog
            column_count = len(columns)
            r_dict = {}
            for index in range(0, column_count):
                r_dict[columns[index]] = r_get[columns[index]]

            yield r_dict

            total_records = total_records + 1

        if r_list['next'] == None:
            has_more = False
        else:
            list_endpoint = r_list['next']




def sample_data(input_stream_id, columns):
    stream_path = input_stream_id[:-1]
    endpoint = 'https://my.15five.com/api/public/' + stream_path
    headers = {'Authorization': 'Bearer ' + '329844b0fc7d43f8bb5b56e1abce2b0c' }

    r_list = requests.get(endpoint, headers=headers)
    r_list = r_list.json()

    data = r_list['results']

    print(data[0])

# sample_data()
