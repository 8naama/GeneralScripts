#################################################################################
# find_jira has function that make specific JQL queries to find relevant jira
# tickets which match the given query.
#################################################################################
import requests
import json
from config import ATLASSIAN_API_TOKEN

# request params
url = "https://logzio.atlassian.net/rest/api/3/search"
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": ATLASSIAN_API_TOKEN}


def get_jira_issues(jql_query, results_limit=None):
    """
    returning object of jira issues that match the provided JQL query.
    :param jql_query: the query to search issues for.
    :param results_limit: the maximum amount of results to return, if None - returns 50 possible results by default.
    :return: dictionary with jira issues.
    """
    print(f"Got request at get_jira_issues function. Amount of expected results are {results_limit}", {'query': jql_query})

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
        if r.text:
            return json.loads(r.text)

    except Exception as e:
        print(f"Got exception {e} at get_jira_issues function for query {jql_query}.")

    return {}


def get_jira_zendesk(jql_query, results_limit=None):
    """
    Returning an array with jira id as well as the Zendesk tickets linked to it.
    :param jql_query: the query to search issues for.
    :param results_limit: the maximum amount of results to return, if None - returns 50 possible results by default.
    :return: dictionary with structure {jira issues: [zendesk tickets ids]};
             for example: {"DEV-123": ["12345", "67890"]}.
    """
    zendesk_per_issue = {}
    zendesk_ticket_ids = []

    jira_array = get_jira_issues(jql_query, results_limit)

    if jira_array:
        if jira_array.get("issues"):
            for issue in jira_array.get("issues"):
                issue_name = issue.get("key")
                zendesk_tickets = issue.get("fields").get("customfield_11705")\

                if zendesk_tickets:
                    zendesk_tickets = zendesk_tickets.get("content")
                    for ticket in zendesk_tickets:
                        content = ticket.get("content")
                        for obj in content:
                            zendesk_ticket_ids = (obj.get("text").split(","))

                zendesk_per_issue[issue_name] = zendesk_ticket_ids
                zendesk_ticket_ids = []

    return zendesk_per_issue
