from uuid import uuid4

from employee.models import Piecework


def piecework_create_bulk(results, daily_works, works_dict, employees_map):
    """Create Piecework records for a successful DailyWork batch."""
    group_id = str(uuid4())
    for data in results:
        work_id = data["work_id"]
        emp_id = data["employee_id"]

        data["daily_work"] = daily_works.get(work_id)
        data["group_id"] = group_id

        emp_obj = employees_map.get(str(emp_id))
        work_obj = works_dict.get(str(work_id))

        # Snapshot fields
        data["employee_name"] = getattr(emp_obj, "name", None)
        data["work_name"] = getattr(work_obj, "work_name", None)
        data["department"] = getattr(emp_obj, "department", None)

        Piecework.objects.create(**data)
