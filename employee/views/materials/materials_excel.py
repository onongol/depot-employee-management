from .materials_filtered import materials_filtered
from employee.utils.export_excel import export_to_excel
from django.db.models import Sum


def export_materials_excel(request):
    """Export calculation materials data to Excel."""
    # Get filtered materials data
    pieceworks = materials_filtered(request)

    # Prepare data for Excel
    headers = [
        "Date",  "Work Name", "Type Material", "Amount Material"
    ]

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

    data.append(["Total", "", "", total_amount])

    return export_to_excel(data, headers, "materials.xlsx", "Materials")
