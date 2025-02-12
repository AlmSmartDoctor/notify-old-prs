import os
import json
from config.repos import ORGANIZATION, REPOS
from src.clients.github import GitHubClient
from src.clients.slack import SlackClient
from src.services.pr_service import PRService
from src.utils.date import calculate_date_days_ago
from src.utils.filter import filter_old_prs, filter_draft_prs

def get_environment_variables():
    return (
        os.environ["GITHUB_TOKEN"],
        os.environ["SLACK_BOT_TOKEN"],
        json.loads(os.environ["SLACK_CHANNEL_IDS"])
    )

def main() -> None:
    github_token, slack_token, channel_ids = get_environment_variables()
    github_client = GitHubClient(github_token)
    slack_client = SlackClient(slack_token)
    seven_days_ago = calculate_date_days_ago(7)
    all_old_pulls = []

    for group, repo_titles in REPOS.items():
        for repo_title in repo_titles:
            try:
                pulls = github_client.get_open_prs(f"{ORGANIZATION}/{repo_title}")
                old_pulls = filter_old_prs(filter_draft_prs(pulls), seven_days_ago)
                for pr in old_pulls:
                    pr["group"] = group
                all_old_pulls.extend(old_pulls)
            except Exception as e:
                print(f"Error fetching PRs for {ORGANIZATION}/{repo_title}: {e}")
                continue

        if all_old_pulls:
            message = PRService.build_message(all_old_pulls)
            slack_client.send_message(channel_ids[group], message)
            all_old_pulls = []

if __name__ == "__main__":
    main()