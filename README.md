### Continuous Sample Collection
Pair of scripts to continuously collect Sample IDs as submitted samples are processed. 

The first script (01_get_sids.py) fetches all samples that are in a state of 'run'. This indicates the sample has been submitted and it is actively being processed in a VM. The script will then touch an empty file with the name matching the Sample ID. The second script (02_query_sids.py) collects Sample IDs from the empty files and queries for status of those Sample IDs. Once the state changes from ‘run’ to ‘succ’ it will fetch the threat score of the sample and remove the empty file associated with the Sample ID. 

### Usage

Setup 01_get_sids.py to run on a cron ever minute
Setup 02_query_sids.py to run on a cron every 5 minutes
