from django.db import transaction

from employee.services.admin_log_entries import log_object_deletions


def delete_queryset_with_admin_log(user, queryset):
    """Delete a queryset and write matching admin LogEntry rows in one transaction."""

    records = list(queryset)
    count = len(records)
    if not records:
        return 0, {}

    with transaction.atomic():
        log_object_deletions(user, records)
        for obj in records:
            obj.delete()

    return count, {}
