from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH
from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_wagon
from employee.utils.totals import calc_totals
from employee.views.wagon.group.group_and_sort import group_and_sort_wagons
from employee.views.wagon.wagon_export.build_headers import build_headers
from employee.views.wagon.wagon_export.build_totals_row import build_totals_row
from employee.views.wagon.wagon_export.format_data import iter_rows
from employee.views.wagon.wagon_prepare import wagon_prepare


def wagon_export_excel(request):
    (
        dailyworks,
        wagon_number,
        type_wagon,
        work_name,
        type_work,
        range_date,
        department,
        group,
        month,
        year,
        month_period,
        order_by,
        direction,
    ) = wagon_prepare(request)

    dailyworks = filter_wagon(
        dailyworks,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        work_name=work_name,
        type_work=type_work,
        range_date=range_date,
    )

    totals = calc_totals(dailyworks)

    wagon_data = group_and_sort_wagons(
        dailyworks,
        group=group,
        month=month,
        year=year,
        order_by=order_by,
        direction=direction,
    )

    headers = build_headers(group=group)
    data = list(iter_rows(wagon_data, group=group))

    data.append(build_totals_row(totals, group=group))

    file_name = "wagon.xlsx"
    sheet_title = str(_("Wagon"))

    meta = {
        GROUP_MONTH: ("wagon_work_monthly.xlsx", _("Monthly Work for Wagons")),
    }

    file_name, title = meta.get(
        group, ("wagon_work_daily.xlsx", _("Daily Work for Wagons"))
    )
    sheet_title = str(title)

    return export_to_excel(data, headers, file_name, sheet_title)
