import logging
from datetime import datetime

from django.utils.dateparse import parse_date

logger = logging.getLogger(__name__)


def format_date(date_str):
    """Helper function to format datetime.date objects into strings."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            # .date() drops the time, so no naive datetime escapes this call.
            return datetime.strptime(date_str, fmt).date()  # noqa: DTZ007
        except ValueError:
            continue
    return None


def parse_date_range(range_date):
    """Parse a date range string into start and end date objects."""
    range_str = (range_date or "").strip()
    if not range_str:
        return None, None

    # Only a real but non-existent date raises here; an unparsable string just
    # comes back as None. Anything else escaping would be our own bug.
    try:
        # Try known separators
        for sep in (" to ", " - ", "–", "—"):
            if sep in range_str:
                start_str, end_str = [
                    date_obj.strip() for date_obj in range_str.split(sep, 1)
                ]
                start = parse_date(start_str)
                end = parse_date(end_str)
                return (start, end) if start and end else (None, None)

        # Single date -> same start/end
        single = parse_date(range_str)
    except ValueError:
        logger.warning("Invalid date range: %s", range_date)
        return None, None

    return (single, single) if single else (None, None)
