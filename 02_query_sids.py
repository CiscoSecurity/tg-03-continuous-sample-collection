import os
import sys
import json
import configparser
import requests


def get(url, **params):
    """ GET the URL and return decoded JSON"""
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error_message:
        sys.exit(error_message)


def post(url, data):
    """ POST to the URL and return decoded JSON"""
    try:
        response = session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error_message:
        sys.exit(error_message)


def threat_query(_host_name, _sample_id):
    threat_url = 'https://{}/api/v2/samples/{}/threat'.format(_host_name, _sample_id)
    return get(threat_url)


def state_query(_host_name, sample_ids):
    data = {'ids':json.dumps(sample_ids)}
    state_url = 'https://{}/api/v2/samples/state'.format(_host_name)
    return post(state_url, data=data)


# Create RESULTS directory if it does not exist
if not os.path.exists('RUNNING'):
    os.makedirs('RUNNING')

# Specify the config file
config_file = 'api.cfg'

# Reading the config file to get settings
config = configparser.ConfigParser()
config.read(config_file)
api_key = config.get('Main', 'api_key')
host_name = config.get('Main', 'host_name')

session = requests.session()
auth_param = {'api_key': api_key}
session.params.update(auth_param)

recent_sample_ids = os.listdir("RUNNING")

if recent_sample_ids:
    status = state_query(host_name, recent_sample_ids)

    for sample in status['data']:
        state = sample['state']
        sample_id = sample['sample']
        if state == 'succ':
            print(threat_query(host_name, sample_id)['data']['score'], sample_id)
            os.remove('RUNNING/{}'.format(sample_id))
