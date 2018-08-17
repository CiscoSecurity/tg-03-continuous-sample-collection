import os
import datetime
import configparser
import requests

# Specify the config file
configFile = 'api.cfg'

# Reading the config file to get settings
config = configparser.RawConfigParser()
config.read(configFile)

api_key = config.get('Main', 'api_key')
api_key = str.rstrip(api_key)

hostName = config.get('Main', 'hostName')
hostName = str.rstrip(hostName)

# Create RESULTS directory if it does not exist
if not os.path.exists('RUNNING'):
    os.makedirs('RUNNING')

def get(query):
    try:
        r = requests.get(query)
        if not r.status_code // 100 == 2:
            return "Error: {}".format(r)
        return r.json()
    except requests.exceptions.RequestException as e:
        return 'Error: %s' % (e)

def sampleQuery():
    baseUrl = 'https://%s/api/v2/samples?org_only=True&api_key=%s&after=last%%20hour' % (hostName, api_key)
    return baseUrl

current_samples = get(sampleQuery())

for sample in current_samples['data']['items']:
    if sample['state'] == 'run':
        SID = sample['id']
        print(SID,'is running')
        os.system("touch RUNNING/"+SID)