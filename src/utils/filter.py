from datetime import datetime
from typing import List, Dict, Any

def filter_old_prs(pulls: List[Dict[str, Any]], threshold_date: datetime) -> List[Dict[str, Any]]:
    return [pr for pr in pulls if datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ") <= threshold_date]

def filter_draft_prs(pulls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [pr for pr in pulls if not pr["draft"]]
