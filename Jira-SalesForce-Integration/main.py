from find_jira import get_jira_zendesk
from get_zendesk_and_intercom_info import get_zendesk_salesforce_id
from config import QUERY

def main():
    jira_zendesk_dic = get_jira_zendesk(QUERY)

    for jira_issue in jira_zendesk_dic:
        salesforce_ids = []
        zendesk_array = jira_zendesk_dic[jira_issue]

        for zendesk_ticket in zendesk_array:
            salesforce_ids.append(get_zendesk_salesforce_id(zendesk_ticket))
        jira_zendesk_dic[jira_issue] = salesforce_ids
    return jira_zendesk_dic


if __name__ == '__main__':
    main()
