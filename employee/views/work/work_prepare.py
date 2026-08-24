from employee.models import Work
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.views.work.work_context import WorkContext


def work_prepare(request) -> WorkContext:
    department = get_selected_department(request)

    works = Work.objects.for_user(request.user)
    if department:
        works = works.filter(department=department)

    job_title = request.GET.get("job_title")
    work_name = request.GET.get("work_name")
    type_wagon = request.GET.get("type_wagon")
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    job_titles = get_distinct_values(Work, "job_title", department)
    type_wagons = get_type_wagon_filter_values(department, source_model="work")

    return WorkContext(
        works=works,
        selected_department=department,
        job_title=job_title,
        work_name=work_name,
        type_wagon=type_wagon,
        order_by=order_by,
        direction=direction,
        job_titles=job_titles,
        type_wagons=type_wagons,
    )
