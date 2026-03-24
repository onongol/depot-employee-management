from django.utils.translation import gettext_lazy as _


def get_bulk_preview_items(qs, count, limit=10):
    """Generates a preview list and summary tail for bulk action messages, limiting displayed items for user-friendly feedback."""
    items = [str(obj) for obj in qs[:limit]]
    tail = "" if count <= limit else _(" ... and %(n)s more") % {"n": count - limit}
    return items, tail
