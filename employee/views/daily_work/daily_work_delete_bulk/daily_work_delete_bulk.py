from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from employee.services.admin_log_delete import delete_queryset_with_admin_log
from employee.utils.parse_ids import parse_ids
from employee.utils.select_department import get_selected_department
from employee.views.daily_work.daily_work_delete_bulk.bulk_queryset import (
    get_bulk_daily_work_qs,
)
from employee.views.daily_work.daily_work_delete_bulk.messages_bulk_preview import (
    preview_daily_work_items,
)


@require_POST
@login_required
@permission_required("employee.delete_dailywork")
def daily_work_delete_bulk(request):
    """
    This code implements a secure and user-friendly bulk delete operation for DailyWork records.
    It validates user input, efficiently fetches related data, generates a detailed preview message for the user, and performs the deletion in a single transaction.
    The approach ensures good UX, prevents accidental deletions, and avoids performance issues by using optimized querysets.
    """
    department = get_selected_department(request)
    fallback_url = reverse("daily_work_list")
    ids = parse_ids(request.POST.getlist("daily_work_ids"))

    if not ids:
        messages.warning(request, _("Select at least one record."))
        return redirect(request.headers.get("referer") or fallback_url)

    base_qs = get_bulk_daily_work_qs(ids=ids, department=department)

    parts = preview_daily_work_items(base_qs=base_qs)

    deleted_count, _deleted_details = delete_queryset_with_admin_log(
        request.user, base_qs
    )

    if deleted_count:
        # Escape each part: they carry employee and work names straight from the DB.
        final_message = format_html_join(
            mark_safe("<br>"), "{}", ((part,) for part in parts)
        )
        messages.success(request, final_message)

    return redirect(request.headers.get("referer") or fallback_url)
