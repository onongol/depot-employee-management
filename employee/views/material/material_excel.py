from django.utils.translation import gettext_lazy as _

from employee.utils.filters import filter_material
from employee.utils.export_excel import export_to_excel
from .material_utils import material_prepare, group_and_sum_materials


def material_export_excel(request):
    """Export calculation materials data to Excel."""
    # Get filtered materials data
    daily_works, work_name, type_material, range_date = material_prepare(request)

    # Apply reusable filter function
    daily_works = filter_material(
        daily_works,
        work_name=work_name,
        type_material=type_material,
        range_date=range_date
    )

    # Group and sum materials
    daily_works = group_and_sum_materials(daily_works)

    # Prepare data for Excel
    headers = [
        _("#"),
        _("Type Material"),
        _("Work Name"), 
        _("Amount Material"),
        _("Date"),
    ]

    headers = [str(h) for h in headers]

    # Format data for export to Excel
    data = [
        [   
            i + 1,
            item['work__type_material'] or "",
            item['work__work_name'] or "",
            item['amount_material'] or 0,
            item['work_date'] or "",

        ]
        for i, item in enumerate(daily_works)
    ]

    # Calculate total amount of material
    total_amount = sum(item['amount_material'] for item in daily_works) if daily_works else 0

    total_str = _("Total")
    total_str = str(total_str)
    empty_row = ""

    data.append(
        [total_str] + [empty_row] * 2 + [total_amount] + [empty_row]
    )

    file_name = "material.xlsx"
    
    sheet_title = _("Material")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
