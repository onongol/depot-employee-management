from employee.views.export_excel import export_to_excel
from employee.views.calculation_materials_filtered import calculation_materials_filtered


def export_calculation_materials_excel(request):
    """Export calculation materials data to Excel."""
    pieceworks = calculation_materials_filtered(request)

    # Prepare data for Excel
    headers = [
        "Date", "Type Material", "Work Name", "Amount Material"
    ]

    data = [
        [
            item.work_date,
            item.work.type_material,
            item.work.work_name,
            item.amount_material,
        ]
        for item in pieceworks
    ]

    return export_to_excel(data, headers, "calculation_materials.xlsx", "Calculation Materials")
