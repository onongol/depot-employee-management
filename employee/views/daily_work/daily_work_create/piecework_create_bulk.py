from uuid import uuid4

from employee.models import Piecework


def piecework_create_bulk(results, daily_works, works_dict, employees_map):
    """Create Piecework records for a successful DailyWork batch."""

    group_id = str(uuid4())

    for data in results:
        work_id = data["work_id"]
        emp_id = data["employee_id"]

        data["daily_work"] = daily_works.get(work_id)
        data["employee"] = employees_map.get(str(emp_id))
        data["work"] = works_dict.get(str(work_id))

        data["group_id"] = group_id

        Piecework.objects.create(**data)
