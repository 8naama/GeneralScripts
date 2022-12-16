# Find Saved Objects with Leading Wildcards
This script queries the provided indexes to find all Kibana Saved Obejcts, and checks which of them contains the provided regex pattern (deafult: finding leading wildcards).

## Prerequisites
You will need python 3 with the following packages:
- re
- requests
- json
- csv
- mysql-connector-python

## Setup
1. Update the `config.py` file if needed:
	- `CLUSTER_LIST` - List of Clusters you want to check Saved Objects of.
	- `CSV_FILE_PATH` - Path where info regarding the problematic saved objects will be written to in CSV format.
	- `SIZE` - The amount of Saved Objects to get from each Cluster every call.
	- `QUERY_REGEX` - Saved Objects whose Queries match the given regex here will be returned by the script. 
	- `FILTER_REGEX` - Saved Objects whose Filters match the given regex here will be returned by the script.
2. Open Terminal and move inside the script directory.
3. run the script with:
```bash
python3 main.py
```

## Note
Please note that the more Clusters you add and the larger the `SIZE` paramter, the longer the script will take to run.
