#################################################################################
# find_jira has function that make specific JQL queries to find relevant jira
# tickets which match the given query.
#################################################################################
import os
import requests
import json
ATLASSIAN_API_TOKEN = os.environ.get("ATLASSIAN_API_TOKEN")

# request params
url = "https://logzio.atlassian.net/rest/api/3/search"
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": ATLASSIAN_API_TOKEN}


def get_jira_issues(jql_query, results_limit=None):
    """
    returning list of issue id's that match the provided JQL query.
    :param jql_query: the query to search cards for.
    :param results_limit: the maximum amount of results to return, if None - returns 50 possible results by default.
    :return: list of issues id's that match the given query.
    """
    issues_id_list = []
    print(f"Got request at get_jira_issues function. Amount of expected results are {results_limit}" , {'query': jql_query})

    # JQL Query to find relevant Jira's
    if results_limit:
        payload = json.dumps({
            "jql": jql_query,
            "maxResults": results_limit
        })
    else:
        # results_limit is None
        payload = json.dumps({
            "jql": jql_query
        })

    # the request
    try:
        r = requests.post(url=url, headers=headers, data=payload)
    except Exception as e:
        print(f"Got exception {e} at get_jira_issues function for query {jql_query}.")

    if r.text:
        if json.loads(r.text).get("issues"):
            for obj in json.loads(r.text).get("issues"):
                issues_id_list.append(obj.get("id"))

    return issues_id_list