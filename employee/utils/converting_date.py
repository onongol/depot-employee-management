from datetime import datetime
import logging
from django.utils.dateparse import parse_date


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


def parse_date_range(range_date):
    """
    Parse date range string 'YYYY-MM-DD to YYYY-MM-DD' and return (start_date, end_date).
    Returns (None, None) if parsing fails.
    """
    try:
        start_str, end_str = [d.strip() for d in range_date.split('to')]
        return parse_date(start_str), parse_date(end_str)
    except Exception as e:
        logging.warning(f'Invalid date range: {range_date} ({e})')
        return None, None
