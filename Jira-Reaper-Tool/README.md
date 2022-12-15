# Jira reaper tool
This script queries the Jira API and Logz.io support API to bulk tag Jira issues with 'SupportReaperCandidates' or 'reaper_stale_item' label and add relevant people as watchers.

## Prerequisites
You will need python 3 with the following packages:
- requests
- json
- os

## Repacing the queries 
If there is a need to update the queries the script is looking Jira issues based on, all you need to do is update the JQL query in main.py.
Relevant variables are:
- QUERY_FOR_REAPER_CANDIDATE
- QUERY_FOR_JIRA_TO_CLOSE

## Note
If there are many Issues that need updating the script might take a minute or two to finish.