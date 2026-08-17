from datetime import date
from decimal import Decimal

import factory
from factory.django import DjangoModelFactory

from employee.constants.constants import Department, JobTitle, TypeWork
from employee.models import DailySalary, DailyWork, Employee, Piecework, Work


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    employee_id = factory.Sequence(lambda n: n + 1)
    employee_name = factory.Sequence(lambda n: f"Employee {n}")
    department = Department.ZASVAR_1.value
    job_title = JobTitle.ZASVARCHIN.value
    money_per_hour = Decimal("2500.00")


class WorkFactory(DjangoModelFactory):
    class Meta:
        model = Work

    work_name = factory.Sequence(lambda n: f"Work {n}")
    department = Department.ZASVAR_1.value
    job_title = JobTitle.ZASVARCHIN.value
    standard_time = Decimal("1.000000")
    price = Decimal("1000.00")


class DailyWorkFactory(DjangoModelFactory):
    class Meta:
        model = DailyWork

    work = factory.SubFactory(WorkFactory)
    job_title = JobTitle.ZASVARCHIN.value
    type_work = TypeWork.TYPE_84.value
    amount = Decimal("1.00")
    work_date = factory.LazyFunction(date.today)


class DailySalaryFactory(DjangoModelFactory):
    class Meta:
        model = DailySalary

    employee = factory.SubFactory(EmployeeFactory)
    hours_per_day = 11
    salary_date = factory.LazyFunction(date.today)


class PieceworkFactory(DjangoModelFactory):
    class Meta:
        model = Piecework

    employee = factory.SubFactory(EmployeeFactory)
    work = factory.SubFactory(WorkFactory)
    job_title = JobTitle.ZASVARCHIN.value
    type_work = TypeWork.TYPE_84.value
    amount = Decimal("1.00")
    work_date = factory.LazyFunction(date.today)
