import logging
from datetime import datetime

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
    Parse date range and return (start_date, end_date).
    Supports:
      - 'YYYY-MM-DD to YYYY-MM-DD'
      - 'YYYY-MM-DD - YYYY-MM-DD'
      - single 'YYYY-MM-DD' (treated as start=end)
    Returns (None, None) if parsing fails.
    """
    try:
        range_str = (range_date or "").strip()
        if not range_str:
            return None, None

        # Try known separators
        for sep in (' to ', ' - ', '–', '—'):
            if sep in range_str:
                start_str, end_str = [date_obj.strip() for date_obj in range_str.split(sep, 1)]
                start = parse_date(start_str)
                end = parse_date(end_str)
                return (start, end) if start and end else (None, None)

        # Single date -> same start/end
        single = parse_date(range_str)
        if single:
            return single, single

        return None, None
    
    except Exception as e:
        logging.warning(f'Invalid date range: {range_date} ({e})')
        return None, None
