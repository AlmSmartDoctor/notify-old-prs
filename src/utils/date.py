from datetime import datetime, timedelta

def calculate_date_days_ago(days: int) -> datetime:
    return datetime.now() - timedelta(days=days)
