# Jira SalesForce Integration
This script queries the Jira, Zendesk and Intercom API to find the SalesForce id of companies who opened a Zendesk ticket that is linked to specific Jira tickets.

## Prerequisites
You will need python 3 with the following packages:
- requests
- json

## Setup
1. Update the `config.py` file with your API tokens and relevant JQL query.
2. run the script with:
```bash
python3 main.py
```
