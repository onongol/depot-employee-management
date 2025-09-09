from datetime import datetime


def format_date(date_str):
    """Helper function to format datetime.date objects into strings."""
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d', '%B %d, %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None
