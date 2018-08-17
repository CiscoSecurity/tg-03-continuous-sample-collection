import os
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

def formatSIDS ( SIDS ):
    formatted = ''
    for SID in running_sids:
        formatted = formatted+"\"%s\"," % SID
    formatted = '['+formatted[:-1]+']'
    return formatted

def get( query ):
    try:
        r = requests.get(query)
        if not r.status_code // 100 == 2:
            return "Error: {}".format(r)
        return r.json()
    except requests.exceptions.RequestException as e:
        return 'Error: %s' % (e)

def threatQuery ( SID ):
    baseUrl = 'https://%s/api/v2/samples/%s/threat?&api_key=%s' % (hostName, SID, api_key)
    return baseUrl

def stateQuery ( SIDS ):
    baseUrl = 'https://%s/api/v2/samples/state?ids=%s&api_key=%s' % (hostName, SIDS, api_key)
    return baseUrl

running_sids = os.listdir("RUNNING")

status = get(stateQuery(formatSIDS(running_sids)))

for sample in status['data']:
    state = sample['state']
    SID = sample['sample']
    if state == 'succ':
        print(get(threatQuery(SID))['data']['score'])
        os.remove('RUNNING/'+SID)