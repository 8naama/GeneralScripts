#################################################################################
# The function main() is starting the script.
# Support Jira reaper is a script to help marking and closing old irrelevant
# jira cards.
#################################################################################
from find_jira import get_jira_issues
from support_members_details import get_tier_2_3_jira_account_id
from edit_jira import Issue
from observer import MultiLogger, logz_logger_init

# initiating the logger that send logs to the Support Logz.io account
logz_logger_init()

# initializing variables
QUERY_FOR_REAPER_CANDIDATE = "\"Zendesk Ticket Count[Number]\">0 AND updated <= -90d AND project in (Development, \"INT\") AND status not in (Done, Validated)"
QUERY_FOR_JIRA_TO_CLOSE = "updated <= -90d AND labels in (SupportReaperCandidates)"
RESULTS_LIMIT = 20


def main(event=None, context=None):
    """
    adds relevant labels to old jira issues based on JQL queries.
    """
    print("Starting Support Jira Reaper tool")
    
    """
    step 1 - tag old jira's with 'SupportReaperCandidates' label and add 2nd and 3rd tier as watchers.
    """
    # getting the Jira issues
    reaper_tag_candidates = get_jira_issues(QUERY_FOR_REAPER_CANDIDATE)

    # adding the label and watcher per jira issue
    for issue_id in reaper_tag_candidates:
        jira = Issue(issue_id)

        print(f"Sending request to update jira issue {issue_id}")
        
        jira.add_label("SupportReaperCandidates")
        for jiraId in get_tier_2_3_jira_account_id():
            jira.add_watcher(jiraId)

    """
    step 2 - tag old jira's with 'reaper_stale_item' so they will get closed automatically.
    """
    # getting Jira issue to close
    old_jiras_to_close = get_jira_issues(QUERY_FOR_JIRA_TO_CLOSE, RESULTS_LIMIT)

    for issue_id in old_jiras_to_close:
        jira = Issue(issue_id)

        print(f"Sending request to update jira issue {issue_id}")

        # adding the tag to the jira
        jira.add_label("reaper_stale_item")
    
    print("Finished Support Jira Reaper tool task")