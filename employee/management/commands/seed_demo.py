"""Load demo data for local/portfolio use: employees, masters, payroll staff,
a work catalog, and a week of daily-work/piecework/salary history.

Idempotent: re-running does not create duplicates or touch existing rows.
Dates are relative to today, so the demo always looks like "this week".
"""

import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    DEPARTMENT_TYPE_WORKS,
    Department,
    JobTitle,
    TypeWagon,
)
from employee.models import (
    DailySalary,
    DailyWork,
    Employee,
    Master,
    Payroll,
    Piecework,
    Work,
)

# Fields: employee_id, name, department, job_title, rank, money_per_hour
EMPLOYEES = [
    (1001, "Батболд Сүхбаатар", Department.MECHANIC, JobTitle.TOKARCHIN, 5, "4500"),
    (1002, "Ганбаатар Эрдэнэ", Department.MECHANIC, JobTitle.GAGNUURCHIN, 4, "4200"),
    (1003, "Дорж Мөнхбат", Department.AKP, JobTitle.ZASVARCHIN, 4, "4000"),
    (1004, "Оюунчимэг Баяр", Department.AKP, JobTitle.ZASVARCHIN, 3, "3800"),
    (1005, "Түмэнбаяр Нэргүй", Department.ZASVAR_1, JobTitle.ZASVARCHIN, 5, "4600"),
    (1006, "Алтангэрэл Хишиг", Department.ZASVAR_1, JobTitle.BUDAGCHIN, 3, "3900"),
    (1007, "Батжаргал Уянга", Department.ZASVAR_2, JobTitle.GAGNUURCHIN, 6, "5200"),
    (1008, "Сарантуяа Золбоо", Department.ZASVAR_2, JobTitle.NEELKHI, 4, "4100"),
    (1009, "Энхбаяр Төмөр", Department.TERGENTSER, JobTitle.ZASVARCHIN, 5, "4700"),
    (1010, "Мөнхжин Ганзориг", Department.TERGENTSER, JobTitle.GAGNUURCHIN, 3, "3700"),
    (
        1011,
        "Болормаа Ариунболд",
        Department.AUTO_UGSRAA,
        JobTitle.ZASVARCHIN,
        4,
        "4300",
    ),
    (1012, "Ганзориг Пүрэв", Department.AUTO_UGSRAA, JobTitle.GAGNUURCHIN, 5, "4900"),
    (1013, "Хүслэн Батдорж", Department.HOS_DUGUI, JobTitle.TOKARCHIN, 4, "4400"),
    (1014, "Наранцэцэг Дэлгэр", Department.HOS_DUGUI, JobTitle.ZASVARCHIN, 3, "3600"),
]

# Fields: master_id, name, department
MASTERS = [
    (501, "Пүрэвдорж Батсайхан", Department.MECHANIC),
    (502, "Отгонбаяр Лхагва", Department.AKP),
    (503, "Ням-Осор Ганбат", Department.ZASVAR_1),
    (504, "Цэрэндорж Мягмар", Department.ZASVAR_2),
    (505, "Баасанжав Төгөлдөр", Department.TERGENTSER),
    (506, "Эрдэнэбат Сумъяа", Department.AUTO_UGSRAA),
    (507, "Ганхуяг Даваа", Department.HOS_DUGUI),
]

# Fields: payroll_id, name
PAYROLL_STAFF = [
    (201, "Уранцэцэг Батбаяр"),
    (202, "Нямдорж Сэргэлэн"),
]

# Fields: work_name, department, job_title, standard_time, price, usage_material, type_material, type_wagon
WORKS = [
    (
        "Тэнхлэг эргүүлэх",
        Department.MECHANIC,
        JobTitle.TOKARCHIN,
        "1.5",
        "15000",
        "0",
        None,
        None,
    ),
    (
        "Гагнуурын угсралт",
        Department.MECHANIC,
        JobTitle.GAGNUURCHIN,
        "2.0",
        "22000",
        "0.5",
        "Гагнуурын утас",
        None,
    ),
    (
        "Тоормосны системийн үзлэг",
        Department.AKP,
        JobTitle.ZASVARCHIN,
        "1.0",
        "12000",
        "0",
        None,
        None,
    ),
    (
        "Дугуйн буксны солилт",
        Department.AKP,
        JobTitle.ZASVARCHIN,
        "1.8",
        "18000",
        "1.2",
        "Буксны тос",
        None,
    ),
    (
        "Вагоны их засвар",
        Department.ZASVAR_1,
        JobTitle.ZASVARCHIN,
        "4.0",
        "45000",
        "0",
        None,
        TypeWagon.ICH_ZASVAR,
    ),
    (
        "Будаг шүрших",
        Department.ZASVAR_1,
        JobTitle.BUDAGCHIN,
        "1.2",
        "13000",
        "3.5",
        "Хуванцар будаг",
        TypeWagon.TAVTSANT,
    ),
    (
        "Хананы гагнуур",
        Department.ZASVAR_2,
        JobTitle.GAGNUURCHIN,
        "2.5",
        "27000",
        "0",
        None,
        TypeWagon.BITUU,
    ),
    (
        "Нээлхийн засвар",
        Department.ZASVAR_2,
        JobTitle.NEELKHI,
        "1.6",
        "17000",
        "0",
        None,
        TypeWagon.CHINGELG,
    ),
    (
        "Тэргэнцэрийн голын шалгалт",
        Department.TERGENTSER,
        JobTitle.ZASVARCHIN,
        "2.2",
        "24000",
        "0",
        None,
        None,
    ),
    (
        "Пүршний солилт",
        Department.TERGENTSER,
        JobTitle.GAGNUURCHIN,
        "1.9",
        "21000",
        "0.8",
        "Пүрш",
        None,
    ),
    (
        "Автомат тоормосны угсралт",
        Department.AUTO_UGSRAA,
        JobTitle.ZASVARCHIN,
        "2.7",
        "29000",
        "0",
        None,
        None,
    ),
    (
        "Гагнуурын угсралт-2",
        Department.AUTO_UGSRAA,
        JobTitle.GAGNUURCHIN,
        "2.1",
        "23000",
        "0",
        None,
        None,
    ),
    (
        "Хос дугуйн эргэлт шалгах",
        Department.HOS_DUGUI,
        JobTitle.TOKARCHIN,
        "1.3",
        "14000",
        "0",
        None,
        None,
    ),
    (
        "Дугуйн голын солилт",
        Department.HOS_DUGUI,
        JobTitle.ZASVARCHIN,
        "1.7",
        "16000",
        "1.0",
        "Голын тос",
        None,
    ),
]

DEMO_DAYS_BACK = 7
# Fixed seed: quantities differ but stay the same across runs (get_or_create
# skips existing rows anyway, so this only matters on --reset).
RANDOM_SEED = 2026


class Command(BaseCommand):
    help = "Load demo employee/work/payroll data for the current week (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Wipe existing demo-covered tables before loading.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Piecework.objects.all().delete()
            DailyWork.objects.all().delete()
            DailySalary.objects.all().delete()
            Work.all_objects.all().delete()
            Employee.all_objects.all().delete()
            Master.all_objects.all().delete()
            Payroll.all_objects.all().delete()
            self.stdout.write("Demo-covered tables cleared.")

        random.seed(RANDOM_SEED)
        created = {
            "employees": 0,
            "masters": 0,
            "payroll": 0,
            "works": 0,
            "daily_work": 0,
            "piecework": 0,
            "daily_salary": 0,
        }

        employees_by_dept = {}
        for employee_id, name, dept, job_title, rank, rate in EMPLOYEES:
            employee, is_new = Employee.objects.get_or_create(
                employee_id=employee_id,
                defaults={
                    "employee_name": name,
                    "department": dept.value,
                    "job_title": job_title.value,
                    "rank": rank,
                    "money_per_hour": Decimal(rate),
                },
            )
            created["employees"] += is_new
            employees_by_dept.setdefault(dept.value, []).append(employee)

        for master_id, name, dept in MASTERS:
            _, is_new = Master.objects.get_or_create(
                master_id=master_id,
                defaults={"master_name": name, "department": dept.value},
            )
            created["masters"] += is_new

        for payroll_id, name in PAYROLL_STAFF:
            _, is_new = Payroll.objects.get_or_create(
                payroll_id=payroll_id,
                defaults={"payroll_name": name},
            )
            created["payroll"] += is_new

        works_by_dept = {}
        for name, dept, job_title, std_time, price, usage, material, wagon in WORKS:
            work, is_new = Work.objects.get_or_create(
                department=dept.value,
                work_name=name,
                defaults={
                    "job_title": job_title.value,
                    "standard_time": Decimal(std_time),
                    "price": Decimal(price),
                    "usage_material": Decimal(usage),
                    "type_material": material,
                    "type_wagon": wagon.value if wagon else None,
                },
            )
            created["works"] += is_new
            works_by_dept.setdefault(dept.value, []).append(work)

        today = timezone.localdate()
        for day_offset in range(DEMO_DAYS_BACK):
            work_date = today - timedelta(days=day_offset)

            for dept, works in works_by_dept.items():
                type_work_choices = DEPARTMENT_TYPE_WORKS[dept]
                type_work = type_work_choices[day_offset % len(type_work_choices)]
                work = works[day_offset % len(works)]
                wagon_number = (
                    f"В-{1000 + day_offset}"
                    if dept in ALLOWED_WAGON_DEPARTMENTS
                    else None
                )

                daily_work, is_new = DailyWork.objects.get_or_create(
                    work=work,
                    work_date=work_date,
                    type_work=type_work,
                    defaults={
                        "amount": Decimal(random.randint(2, 6)),  # noqa: S311
                        "wagon_number": wagon_number,
                    },
                )
                created["daily_work"] += is_new

                for employee in employees_by_dept.get(dept, []):
                    _, is_new = Piecework.objects.get_or_create(
                        employee=employee,
                        work=work,
                        work_date=work_date,
                        defaults={
                            "daily_work": daily_work,
                            "type_work": type_work,
                            "wagon_number": wagon_number,
                            "amount": Decimal(random.randint(1, 3)),  # noqa: S311
                        },
                    )
                    created["piecework"] += is_new

                    _, is_new = DailySalary.objects.get_or_create(
                        employee=employee,
                        salary_date=work_date,
                        defaults={
                            "hours_per_day": random.choice([8, 9, 10, 11])  # noqa: S311
                        },
                    )
                    created["daily_salary"] += is_new

                # Piecework.amount_price defaults to a placeholder until synced;
                # re-saving the DailyWork runs the same sync a real edit would,
                # now that DailySalary rows exist to split its price by.
                daily_work.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data loaded. Created: "
                f"{created['employees']} employees, "
                f"{created['masters']} masters, "
                f"{created['payroll']} payroll staff, "
                f"{created['works']} works, "
                f"{created['daily_work']} daily-work records, "
                f"{created['piecework']} piecework records, "
                f"{created['daily_salary']} daily-salary records."
            )
        )
