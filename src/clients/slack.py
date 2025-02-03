import requests

class SlackClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        }

    def send_message(self, channel_id: str, text: str) -> None:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=self.headers,
            json={"channel": channel_id, "text": text}
        )
        
        if not response.json().get("ok"):
            raise Exception(f"Slack API Error: {response.json()}")