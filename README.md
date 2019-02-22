[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Threat-Grid "Gitter chat")

### Threat Grid Continuous Sample Collection:
Pair of scripts to continuously collect Sample IDs as submitted samples are processed. 

The first script (01_get_sids.py) fetches all samples that are in a state of 'wait'. This indicates the sample has been submitted and has not completed analysis. The script then touches an empty file with the name matching the Sample ID.

The second script (02_query_sids.py) collects Sample IDs from the empty files and queries for status of those Sample IDs. Once the state changes to ‘succ’ it will fetch the threat score of the sample and remove the empty file associated with the Sample ID. 

### Before using you must update the following:
The authentication parameters are set in the ```api.cfg``` :
- api_key

### Usage:
Setup 01_get_sids.py to run on a cron every minute
Setup 02_query_sids.py to run on a cron every 5 minutes

### Example script output:
When executed by a cron job there will be no visable output
