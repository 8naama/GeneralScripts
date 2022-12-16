import re
import requests
import json
import csv
import mysql.connector
from config import SIZE, CSV_FILE_PATH, QUERY_REGEX, FILTER_REGEX, DB_CONNECTIONS, DB_USERNAME, DB_PASSWORD


def get_saved_objects(cluster):
    """
    Finding all the saved objects in the given cluster.
    :param cluster: the name of cluster to search on
    :return: array with all saved objects in the cluster.
    """
    saved_objects = []
    url = f"http://{cluster}:9200/kibana-logz-*/_search?q=type:(search OR visualization OR dashboard)&size={SIZE}"
    try:
        response = json.loads(requests.get(url=url).text)
        saved_objects = response.get("hits").get("hits")

    except Exception as e:
        print(f"Failed to get saved objects from cluster {cluster} duo to error {e}")

    return saved_objects


def get_region(cluster):
    """
    Returns the region the given cluster is on.
    :param cluster: the name of cluster.
    :return: the region the given cluster is on.
    """
    region = None
    pattern = re.compile("^(es-\w+-\d+\.\w+\.|elasticsearch-\d+\.\w+\.)(?P<region>.*?)\.")

    try:
        region = pattern.search(cluster).group("region")

    except AttributeError:
        print(f"Failed to find region in given cluster name {cluster}.")
    except Exception as e:
        print(f"Failed to find region in given cluster name {cluster}. duo to unexpected error {e}.")

    return region


def get_object_query(raw_saved_object_json):
    """
    finding the query and filters used by the saved object.
    :return: array with the query and an array of filters (if no filters it would be an empty array).
    """
    query = None
    filters = None

    try:
        kibana_request = json.loads(raw_saved_object_json.get("kibanaSavedObjectMeta").get("searchSourceJSON"))
        query = kibana_request.get("query")
        filters = kibana_request.get("filter")

    except AttributeError:
        print(f"Failed to get Kibana Query Request for {raw_saved_object_json}")
    except Exception as e:
        print(f"Failed to get Kibana Query duo to unexpected error {e} for {raw_saved_object_json}")

    return [query, filters]


def get_account_id(region, index):
    """
    Returns the account id of the account that has the given index.
    :param region: the account region.
    :param index: the index to find account id for.
    :return: the account id.
    """
    try:
        db_connection = mysql.connector.connect(
            host=DB_CONNECTIONS.get(region),
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="lhdb"
        )
        cursor = db_connection.cursor()
        sql_query = f"SELECT account_id FROM account_settings WHERE es_index_prefix LIKE '%{index}%'"

        cursor.execute(sql_query)
        results = cursor.fetchone()

        cursor.close()
        db_connection.close()

        if results:
            return results[0]  # the account id
    except Exception as e:
        print("Failed to get account id duo to error", e)
    return index


def is_heavy(query, filters):
    """
    Checks if the provided query and filters considered heavy (greedy).
    :param query: a query to check if heavy
    :param filters: an array of filters to check if heavy
    :return: array with boolean (True for heavy query, False for not heavy), heavy query and heavy filters (if found)
    """
    heavy = False
    heavy_query = None
    heavy_filters = []

    if query:
        query_string = str(query.get("query"))
        pattern = re.compile(QUERY_REGEX)

        try:
            greedy_query = pattern.search(query_string)
            if greedy_query:
                heavy = True
                heavy_query = query_string

        except Exception as e:
            print(f"Failed to search for greedy query at {query} duo to error {e}.")

    if filters:
        pattern = re.compile(FILTER_REGEX)

        try:
            for fltr in filters:
                greedy_filter = pattern.search(str(fltr))

                if greedy_filter:
                    heavy = True
                    heavy_filters.append(fltr)
        except Exception as e:
            print(f"Failed to search for greedy filters at {filters} duo to error {e}.")

    return heavy, heavy_query, heavy_filters


def write_to_csv(data):
    """
    Writed the provided rows to a CSV file.
    :param data: an array with dictionary which column should get which value in the row.
    :return: -
    """
    fieldnames = ["Account id", "Company Name", "Region", "Cluster", "Saved Object Type", "Name", "Object id",
                  "Last Updated At", "Problematic Query", "Problematic Filters"]

    try:
        with open(CSV_FILE_PATH, "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerows(data)
    except Exception as e:
        print(f"Failed to write data to CSV duo to error {e}")
