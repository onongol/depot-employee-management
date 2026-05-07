from django.db.models import QuerySet
from django.utils.translation import gettext as _


def get_bulk_preview_items(qs: QuerySet, count: int, limit: int = 10):
    """Generates a preview list and summary tail for bulk action messages, limiting displayed items for user-friendly feedback."""
    items = [str(obj) for obj in qs[:limit]]
    tail = "" if count <= limit else _(" ... and %(n)s more") % {"n": count - limit}
    return items, tail
