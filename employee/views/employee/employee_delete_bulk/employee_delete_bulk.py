from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from employee.messages.bulk_delete_messages.blocked_bulk_message import (
    blocked_bulk_message,
)
from employee.messages.bulk_delete_messages.bulk_preview_helpers import (
    get_bulk_preview_items,
)
from employee.messages.bulk_delete_messages.delete_bulk_message import (
    delete_bulk_message,
)
from employee.services.admin_log_delete import delete_queryset_with_admin_log
from employee.utils.access import is_admin
from employee.utils.parse_ids import parse_ids
from employee.utils.select_department import get_selected_department
from employee.views.employee.employee_delete_bulk.selectors import (
    get_deletable_and_blocked_employees,
)


@require_POST
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def employee_delete_bulk(request):
    department = get_selected_department(request)
    fallback_url = reverse("employee_list")
    ids = parse_ids(request.POST.getlist("employee_table_ids"))

    if not ids:
        messages.warning(request, _("Select at least one record."))
        return redirect(request.META.get("HTTP_REFERER") or fallback_url)

    blocked_qs, deletable_qs = get_deletable_and_blocked_employees(ids, department)

    deletable_count = deletable_qs.count()
    deletable_items, deletable_tail = get_bulk_preview_items(
        deletable_qs, deletable_count
    )

    blocked_count = blocked_qs.count()
    blocked_items, blocked_tail = get_bulk_preview_items(blocked_qs, blocked_count)

    deleted_count = 0
    if deletable_qs.exists():
        deleted_count, _deleted_details = delete_queryset_with_admin_log(
            request.user, deletable_qs
        )

    delete_bulk_message(request, deleted_count, deletable_items, deletable_tail)
    blocked_bulk_message(request, blocked_count, blocked_items, blocked_tail)

    return redirect(request.META.get("HTTP_REFERER") or fallback_url)
