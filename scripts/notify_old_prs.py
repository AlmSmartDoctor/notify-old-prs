import os
import json
import requests
from datetime import datetime, timedelta

def get_environment_variables():
    github_token = os.environ["GITHUB_TOKEN"]
    repo_path = os.environ["GITHUB_REPOSITORY"]
    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
    slack_channel_dict = json.loads(os.environ["REPO_SLACK_CHANNEL_MAP"])
    return github_token, repo_path, slack_bot_token, slack_channel_dict

def calculate_date_days_ago(days):
    return datetime.now() - timedelta(days=days)

def get_github_open_prs(repo_path, github_token):
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo_path}/pulls?state=open&per_page=100"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def filter_old_prs(pulls, threshold_date):
    old_pulls = []
    for pr in pulls:
        pr_created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        if pr_created_at < threshold_date:
            old_pulls.append(pr["html_url"])
    return old_pulls

def send_slack_message(slack_bot_token, slack_channel_id, message):
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

def main():
    github_token, repo_path, slack_bot_token, slack_channel_dict = get_environment_variables()
    print(f"slack_channel_dict: {slack_channel_dict}")
    print(f"keys: {slack_channel_dict.keys()}")
    
    repo_name = repo_path.split("/")[1].strip()
    print(f"repo_name: {repo_name}")
    print(f"type of repo_name: {type(repo_name)}")
    
    slack_channel_id = slack_channel_dict.get(str(repo_name), "C07HM1YH0H4")
    print(f"slack_channel_id: {slack_channel_id}")

    seven_days_ago = calculate_date_days_ago(7)
    pulls = get_github_open_prs(repo_path, github_token)
    old_pulls = filter_old_prs(pulls, seven_days_ago)

    if not old_pulls:
        print("7일 이상 된 오픈 PR이 없습니다.")
        return

    message = "*다음 Pull Request들은 7일 이상 오픈 상태입니다:*\n"
    for pr_url in old_pulls:
        message += f"- {pr_url}\n"

    send_slack_message(slack_bot_token, slack_channel_id, message)

if __name__ == "__main__":
    main()

