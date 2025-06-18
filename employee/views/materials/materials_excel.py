from .materials_filtered import materials_filtered
from employee.utils.export_excel import export_to_excel


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
            item.work_date,
            item.work.work_name,
            item.work.type_material,
            item.amount_material,
        ]
        for item in pieceworks
    ]

    return export_to_excel(data, headers, "materials.xlsx", "Materials")
