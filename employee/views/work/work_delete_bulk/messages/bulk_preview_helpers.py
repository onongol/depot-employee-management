from django.utils.translation import gettext_lazy as _


def get_bulk_preview_items(qs, count, limit=10):
    items = [str(work) for work in qs[:limit]]
    tail = "" if count <= limit else _(f" ... and {count - limit} more")
    return items, tail
