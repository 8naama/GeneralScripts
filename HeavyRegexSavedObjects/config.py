#########################
# Search cluster config #
#########################
SIZE = 10000
CLUSTER_LIST = [
    'es-logs-123.prod.ap-northeast-1.internal.XXX'
    'elasticsearch-123.prod.us-east-1.XXX'
]

####################################
# Regex to search in Saved Objects #
####################################
QUERY_REGEX = ":(/\.\*|\*)"
FILTER_REGEX = ":\.\*"

###########################
# File to save results in #
###########################
CSV_FILE_PATH = "<<PATH_TO_SAVE_FILE>>"

########################
# DB connection config #
########################
DB_USERNAME = "<<DB_USERNAME>>"
DB_PASSWORD = "<<DB_PASSWORD>>"
DB_CONNECTIONS = {
    "us-east-1": "<<DB_HOST>>",
    "eu-central-1": "<<DB_HOST>>",
    "ca-central-1": "<<DB_HOST>>",
    "ap-southeast-2": "<<DB_HOST>>",
    "eu-west-2": "<<DB_HOST>>",
    "ap-northeast-1": "<<DB_HOST>>",
    "westeurope": "<<DB_HOST>>",
    "westus2": "<<DB_HOST>>"
}
