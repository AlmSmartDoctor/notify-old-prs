import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

def get_environment_variables() -> Tuple[str, str, str, Dict[str, str]]:
    github_token = os.environ["GITHUB_TOKEN"]
    repo_path = os.environ["GITHUB_REPOSITORY"]
    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
    slack_channel_dict = json.loads(os.environ["REPO_SLACK_CHANNEL_MAP"])

    return github_token, repo_path, slack_bot_token, slack_channel_dict

def calculate_date_days_ago(days: int) -> datetime:
    return datetime.now() - timedelta(days=days)

def get_github_open_prs(repo_path: str, github_token: str) -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo_path}/pulls?state=open&per_page=100"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def filter_old_prs(pulls: List[Dict[str, Any]], threshold_date: datetime) -> List[Dict[str, Any]]:
    old_pulls = []
    for pr in pulls:
        pr_created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        if pr_created_at <= threshold_date:
            old_pulls.append(pr)
    return old_pulls

def send_slack_message(slack_bot_token: str, slack_channel_id: str, message: str) -> None:
    slack_api_url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": slack_channel_id,
        "text": message
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {slack_bot_token}"
    }
    slack_response = requests.post(slack_api_url, headers=headers, json=payload)
    slack_data = slack_response.json()

    if not slack_data.get("ok"):
        raise Exception(f"Slack API Error: {slack_data}")

def build_message(old_pulls: List[Dict[str, Any]]) -> str:
    message = "*다음 Pull Request들은 7일 이상 오픈 상태입니다:*\n"
    for i, pr in enumerate(old_pulls, start=1):
        pr_title = pr["title"]
        pr_url = pr["html_url"]
        pr_created_at_str = pr["created_at"]
        pr_created_at_dt = datetime.strptime(pr_created_at_str, "%Y-%m-%dT%H:%M:%SZ")
        days_open = (datetime.now() - pr_created_at_dt).days

        message += (
            f"{i}. <{pr_url}|{pr_title}>\n"
            f"   └ *열린 날짜*: {pr_created_at_dt.strftime('%Y-%m-%d %H:%M')} "
            f"({days_open}일 전)\n\n"
        )
    
    return message

def main() -> None:
    github_token, repo_path, slack_bot_token, slack_channel_dict = get_environment_variables()
    repo_name = repo_path.split("/")[1].strip()
    slack_channel_id = slack_channel_dict.get(str(repo_name), "C07HM1YH0H4")

    seven_days_ago = calculate_date_days_ago(7)
    pulls = get_github_open_prs(repo_path, github_token)
    old_pulls = filter_old_prs(pulls, seven_days_ago)

    if not old_pulls:
        print("7일 이상 된 오픈 PR이 없습니다.")
        return

    message = build_message(old_pulls)
    send_slack_message(slack_bot_token, slack_channel_id, message)

if __name__ == "__main__":
    main()