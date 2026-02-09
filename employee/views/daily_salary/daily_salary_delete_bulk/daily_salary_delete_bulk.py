from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from employee.utils.access import is_admin
from employee.utils.parse_ids import parse_ids
from employee.utils.select_department import get_selected_department
from employee.views.daily_salary.daily_salary_delete_bulk.daily_salary_selectors import (
    get_deletable_and_blocked_daily_salaries,
)
from employee.views.daily_salary.daily_salary_delete_bulk.messages.blocked_bulk_message import (
    blocked_bulk_message,
)
from employee.views.daily_salary.daily_salary_delete_bulk.messages.bulk_preview_helpers import (
    get_bulk_preview_items,
)
from employee.views.daily_salary.daily_salary_delete_bulk.messages.delete_bulk_messange import (
    delete_bulk_message,
)


@require_POST
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def daily_salary_delete_bulk(request):
    """
    This function handles bulk deletion of DailySalary records selected via checkboxes.
    It prevents deletion if related Piecework records exist, shows user messages for both deleted and blocked items,
    and uses helper utilities for parsing, preview, and messaging to keep the view clean and maintainable.
    """
    department = get_selected_department(request)
    fallback_url = reverse("daily_salary_list")
    ids = parse_ids(request.POST.getlist("daily_salary_ids"))

    if not ids:
        messages.warning(request, _("Select at least one record."))
        return redirect(request.META.get("HTTP_REFERER") or fallback_url)

    blocked_qs, deletable_qs = get_deletable_and_blocked_daily_salaries(ids, department)

    deletable_count = deletable_qs.count()
    deletable_items, deletable_tail = get_bulk_preview_items(deletable_qs, deletable_count)

    blocked_count = blocked_qs.count()
    blocked_items, blocked_tail = get_bulk_preview_items(blocked_qs, blocked_count)

    deleted_count = 0
    if deletable_qs.exists():
        deleted_count, _deleted_details = deletable_qs.delete()

    delete_bulk_message(request, deleted_count, deletable_items, deletable_tail)

    blocked_bulk_message(request, blocked_count, blocked_items, blocked_tail)

    return redirect(request.META.get("HTTP_REFERER") or fallback_url)
