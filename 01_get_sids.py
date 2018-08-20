import os
import sys
import pathlib
import configparser
import requests


def get(url, **params):
    """ GET the URL and return decoded JSON"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error_message:
        sys.exit(error_message)


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

parameters = {'api_key':api_key,
              'after':'last hour',
              'state':'succ',
              'org_only':True}

submission_search_url = f'https://{host_name}/api/v2/search/submissions'

current_samples = get(submission_search_url, **parameters)

for sample in current_samples['data']['items']:
    sample_id = sample['item']['sample']
    print(sample_id)
    pathlib.Path(f'RUNNING/{sample_id}').touch()
