from datetime import datetime
from typing import List, Dict, Any

class PRService:
    @staticmethod
    def build_message(old_pulls: List[Dict[str, Any]]) -> str:
        repo_grouped = {}
        for pr in old_pulls:
            repo_name = pr.get("base", {}).get("repo", {}).get("name", "Unknown Repo")
            repo_grouped.setdefault(repo_name, []).append(pr)
        
        message = "*7일 이상 오픈된 Pull Request 목록:*\n\n"
        for repo, prs in repo_grouped.items():
            message += f"  *{repo}*\n"
            for idx, pr in enumerate(prs, 1):
                created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                days_open = (datetime.now() - created_at).days
                message += (
                    f"    {idx}. <{pr['html_url']}|{pr['title']}>\n"
                    f"       └ 열린 날짜: {created_at.strftime('%Y-%m-%d %H:%M')} ({days_open}일 전)\n"
                )
            message += "\n"
        return message