from datetime import datetime, timedelta
from typing import List, Dict, Any

def calculate_date_days_ago(days: int) -> datetime:
    return datetime.now() - timedelta(days=days)

def filter_old_prs(pulls: List[Dict[str, Any]], threshold_date: datetime) -> List[Dict[str, Any]]:
    return [pr for pr in pulls if datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ") <= threshold_date]