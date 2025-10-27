from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .material_filtered import material_filter, group_and_sum_materials
from employee.utils.export_excel import export_to_excel


def export_material_excel(request):
    """Export calculation materials data to Excel."""
    # Get filtered materials data
    daily_works = material_filter(request)

    # Group and sum materials
    daily_works = group_and_sum_materials(daily_works)

    # Prepare data for Excel
    headers = [
        _("Date"), 
        _("Work Name"), 
        _("Type Material"), 
        _("Amount Material")
    ]

    headers = [str(h) for h in headers]

    # Format data for export to Excel
    data = [
        [
            item['work_date'] or "",
            item['work__work_name'] or "",
            item['work__type_material'] or "",
            item['amount_material'] or 0,
        ]
        for item in daily_works
    ]

    # Calculate total amount of material
    total_amount = sum(item['amount_material'] for item in daily_works) if daily_works else 0

    total_str = _("Total")
    total_str = str(total_str)

    data.append([total_str, "", "", total_amount])

    file_name = "material.xlsx"
    
    sheet_title = _("Material")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
