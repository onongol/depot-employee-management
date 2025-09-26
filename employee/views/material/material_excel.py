from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .material_filtered import material_filter
from employee.utils.export_excel import export_to_excel


def export_material_excel(request):
    """Export calculation materials data to Excel."""
    # Get filtered materials data
    pieceworks = material_filter(request)

    # Prepare data for Excel
    headers = [
        _("Date"), 
        _("Work Name"), 
        _("Type Material"), 
        _("Amount Material")
    ]

    headers = [str(h) for h in headers]

    data = [
        [
            item.work_date or "",
            item.work.work_name or "",
            item.work.type_material or "",
            item.amount_material or 0,
        ]
        for item in pieceworks
    ]

    total_amount = pieceworks.aggregate(total=Sum('amount_material'))['total'] or 0

    total_str = _("Total")
    total_str = str(total_str)

    data.append([total_str, "", "", total_amount])

    file_name = "material.xlsx"
    sheet_title = _("Material")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
