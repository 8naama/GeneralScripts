#################################################################################
# This file has functions to find a user Zendesk and Intercom data based on
# Zendesk ticket id.
#################################################################################
import requests
import json
from config import ZENDESK_API_TOKEN, INTERCOM_API_TOKEN

zendesk_headers = {"Authorization": ZENDESK_API_TOKEN}
intercom_headers = {"Authorization": INTERCOM_API_TOKEN, "Accept": "application/json", "CONTENT-TYPE": "application/json"}


def get_zendesk_ticket(ticket_id):
    """
    Returns the details of given Zendesk ticket.
    :param ticket_id: the Zendesk ticket id
    :return: object with the Zendesk ticket details
    """
    url = f"https://logzio.zendesk.com/api/v2/tickets/{ticket_id}"

    try:
        r = requests.get(url=url, headers=zendesk_headers)
        return json.loads(r.text)
    except Exception as e:
        print(f"Got exception {e} at get_zendesk_ticket function for ticket {ticket_id}.")

    return {}


def get_user_from_zendesk_ticket(ticket_id):
    """
    Returns the user who requested the Zendesk ticket.
    :param ticket_id: the Zendesk ticket id.
    :return: Email of the user who opened the ticket
    """
    user = ""
    ticket_raw_json = get_zendesk_ticket(ticket_id)

    try:
        ticket = ticket_raw_json.get("ticket")
        user_id = ticket.get("requester_id")

        url = f"https://logzio.zendesk.com/api/v2/users/{user_id}/identities"

        r = requests.get(url=url, headers=zendesk_headers)
        user_info_json = json.loads(r.text)
        user_info = user_info_json.get("identities")[0]
        user = user_info.get("value")
    except AttributeError as e:
        print("Failed to get zendesk ticket requester probably duo to failure of a previous function, Exception is ", e)
    except Exception as e:
        print("Failed to get zendesk ticket requester duo to error", e)

    return user


def get_intercom_info(user_email):
    """
    Returns Intercom user data of the given user.
    :param user_email: Email of the user.
    :return: Intercom User Data of given user
    """
    user_info = {}
    url = "https://api.intercom.io/contacts/search"
    request_body = {
        "query": {
            "field": "email",
            "operator": "=",
            "value": user_email
        }
    }

    try:
        r = requests.post(url=url, headers=intercom_headers, data=json.dumps(request_body))

        user_info_json = json.loads(r.text)
        user_info = user_info_json.get("data")[0]
    except Exception as e:
        print("Failed to get Intercom info duo to error", e)
    return user_info


def get_zendesk_salesforce_id(ticket_id):
    """
    Returns the Salesforce id of the Customer Company who requested the Zendesk ticket.
    :param ticket_id: The Zendesk Ticket id
    :return: The Salesforce id of the Company who requested the ticket.
    """
    salesforce_id = ""
    email = get_user_from_zendesk_ticket(ticket_id)
    intercom_info = get_intercom_info(email)

    try:
        user_custom_attributes = intercom_info.get("custom_attributes")
        salesforce_id = user_custom_attributes.get("salesforce_id")
    except AttributeError as e:
        print("Failed to get salesforce id probably duo to failure of a previous function. Exception is", e)
    except Exception as e:
        print("Failed to get salesforce id duo to error", e)

    return salesforce_id
