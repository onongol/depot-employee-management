from datetime import datetime


def parse_date(date_str):
    """Helper function to parse date strings into datetime.date objects."""
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d', '%B %d, %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None
