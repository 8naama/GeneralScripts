#################################################################################
# this file has function that help getting info regarding the support
# team members.
#################################################################################
import os
import requests
import json
SUPPORT_API_TOKEN = os.environ.get("SUPPORT_API_TOKEN")

# requests global params
headers = {"Accept": "application/json"}


def get_tier_2_3_jira_account_id():
    """
    returns the support team tier 2 and 3 jira accountId
    :return: list of 2nd and 3rd tier jira accountId's
    """
    jira_account_ids = []
    # request params;
    url = "https://api.logziosupport.click/members"
    support_api_headers = {"X-API-TOKEN": SUPPORT_API_TOKEN}
    

    # the request to get the team members
    try:
        tier_2 = requests.get(url=url + "?role=Tier2", headers=support_api_headers)
        tier_3 = requests.get(url=url + "?role=Tier3", headers=support_api_headers)
    except Exception as e:
        print(f"Got exception {e} at get_tier_2_3_jira_account_id function.")

    # adding the members jira accountId to the jira_account_ids array
    if tier_2.text:
        for obj in json.loads(tier_2.text):
            jira_account_ids.append(obj['jiraAccountId'])

    if tier_3.text:
        for obj in json.loads(tier_3.text):
            jira_account_ids.append(obj['jiraAccountId'])

    # returning the jira_account_ids array
    return jira_account_ids