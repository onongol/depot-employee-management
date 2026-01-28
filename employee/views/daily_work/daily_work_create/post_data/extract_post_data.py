from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.views.daily_work.daily_work_create.post_data.post_data_context import (
    PostData,
)


def extract_post_data(request) -> PostData:
    work_date = request.POST.get("work_date")
    type_work = request.POST.get("type_work")
    job_title = request.POST.get("job_title")

    raw_wagon_number = (request.POST.get("wagon_number") or "").strip()
    wagon_number = (
        None
        if not raw_wagon_number or raw_wagon_number == DEFAULT_WAGON_NUMBER
        else raw_wagon_number
    )

    selected_employee_ids = request.POST.getlist("employee_ids")
    selected_work_ids = request.POST.getlist("work_ids")

    amounts = {
        work_id: request.POST.get(f"amount_{work_id}")
        for work_id in selected_work_ids
        if request.POST.get(f"amount_{work_id}")
    }

    return PostData(
        work_date=work_date,
        type_work=type_work,
        job_title=job_title,
        wagon_number=wagon_number,
        selected_employee_ids=selected_employee_ids,
        selected_work_ids=selected_work_ids,
        amounts=amounts,
    )
