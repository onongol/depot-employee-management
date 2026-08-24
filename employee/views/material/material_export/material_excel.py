from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext_lazy as _

from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_material
from employee.views.material.material_export.build_headers import build_headers
from employee.views.material.material_export.build_totals_row import build_totals_row
from employee.views.material.material_export.format_data import iter_rows
from employee.views.material.material_grouping import group_and_sum_materials
from employee.views.material.material_prepare import material_prepare


@login_required
@permission_required("employee.view_material_report", raise_exception=True)
def material_export_excel(request):
    """Export calculation materials data to Excel."""
    context = material_prepare(request)

    daily_works = context.daily_works

    daily_works = filter_material(daily_works, context=context)

    daily_works = group_and_sum_materials(daily_works)

    headers = build_headers()

    data = list(iter_rows(daily_works))

    data.append(build_totals_row(daily_works))

    file_name = "material.xlsx"
    sheet_title = str(_("Material"))

    return export_to_excel(data, headers, file_name, sheet_title)
