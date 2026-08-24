from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from employee.messages.bulk_delete_messages.bulk_preview_helpers import (
    get_bulk_preview_items,
)
from employee.messages.bulk_delete_messages.delete_bulk_message import (
    delete_bulk_message,
)
from employee.models.work_models import Work
from employee.services.admin_log_delete import delete_queryset_with_admin_log
from employee.utils.parse_ids import parse_ids
from employee.utils.select_department import get_selected_department


@require_POST
@login_required
@permission_required("employee.delete_work", raise_exception=True)
def work_delete_bulk(request):
    department = get_selected_department(request)
    fallback_url = reverse("work_list")
    ids = parse_ids(request.POST.getlist("work_table_ids"))

    if not ids:
        messages.warning(request, _("Select at least one record."))
        return redirect(request.headers.get("referer") or fallback_url)

    deletable_qs = Work.all_objects.filter(pk__in=ids, department=department)
    deletable_count = deletable_qs.count()
    deletable_items, deletable_tail = get_bulk_preview_items(
        deletable_qs, deletable_count
    )

    deleted_count = 0
    if deletable_qs.exists():
        deleted_count, _deleted_details = delete_queryset_with_admin_log(
            request.user, deletable_qs
        )

    delete_bulk_message(request, deleted_count, deletable_items, deletable_tail)

    return redirect(request.headers.get("referer") or fallback_url)
