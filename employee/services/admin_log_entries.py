import json

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.text import Truncator


def _build_log_entry(user, obj, action_flag, change_message=""):
    if not getattr(user, "is_authenticated", False) or getattr(obj, "pk", None) is None:
        return None

    content_type = ContentType.objects.get_for_model(obj, for_concrete_model=False)
    return LogEntry(
        user_id=user.pk,
        content_type_id=content_type.pk,
        object_id=str(obj.pk),
        object_repr=Truncator(str(obj)).chars(200),
        action_flag=action_flag,
        change_message=change_message,
    )


def log_object_addition(user, obj):
    log_entry = _build_log_entry(user, obj, ADDITION)
    if log_entry is not None:
        log_entry.save()


def log_object_change(user, obj, changed_fields=None):
    change_message = ""
    if changed_fields:
        change_message = json.dumps(
            [{"changed": {"fields": list(changed_fields)}}], ensure_ascii=False
        )

    log_entry = _build_log_entry(user, obj, CHANGE, change_message=change_message)
    if log_entry is not None:
        log_entry.save()


def log_object_deletion(user, obj):
    log_entry = _build_log_entry(user, obj, DELETION)
    if log_entry is not None:
        log_entry.save()


def log_object_additions(user, objects):
    log_entries = [
        log_entry
        for log_entry in (_build_log_entry(user, obj, ADDITION) for obj in objects)
        if log_entry is not None
    ]
    if log_entries:
        LogEntry.objects.bulk_create(log_entries)


def log_object_deletions(user, objects):
    log_entries = [
        log_entry
        for log_entry in (_build_log_entry(user, obj, DELETION) for obj in objects)
        if log_entry is not None
    ]
    if log_entries:
        LogEntry.objects.bulk_create(log_entries)
