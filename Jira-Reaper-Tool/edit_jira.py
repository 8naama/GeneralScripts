#################################################################################
# Class Issue has functions that allow editing and getting relevant data from a
# Jira issue ticket.
#################################################################################
import os
import requests
import json
ATLASSIAN_API_TOKEN = os.environ.get("ATLASSIAN_API_TOKEN")


# request global params
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": ATLASSIAN_API_TOKEN}


class Issue(object):
    def __init__(self, issue_id):
        self.issue_id = issue_id

    def add_label(self, new_label):
        """
        adds a new label to the Jira ticket
        :param new_label: the name of new label to add
        :return: request response
        """
        # request params
        url = f"https://logzio.atlassian.net/rest/api/3/issue/{self.issue_id}"
        payload = json.dumps({
            "update": {
                "labels": [{
                        "add": new_label
                    }]
            }
        })

        # the request
        try:
            r = requests.put(url=url, headers=headers, data=payload)
            print(f"Added '{new_label}' label for jira issue {self.issue_id}")
        except Exception as e:
            print(f"An exception {e} occurred in attempt to add '{new_label}' label for jira issue {self.issue_id}")


    def add_watcher(self, new_watcher):
        """
        adds the given user as watcher to the jira issue
        :param new_watcher: account ID of the user that should be added as new watcher
        :return: the request response
        """
        # request params
        url = f"https://logzio.atlassian.net/rest/api/3/issue/{self.issue_id}/watchers"
        payload = json.dumps(new_watcher)

        # the request
        try:
            r = requests.post(url=url, headers=headers, data=payload)
            print(f"Added {new_watcher} as watcher for jira issue {self.issue_id}")
        except Exception as e:
            print(f"An exception {e} occurred in attempt to add {new_watcher} as watcher for jira issue {self.issue_id}")