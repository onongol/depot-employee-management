from django import forms

from employee.forms.forms_mixins.job_title_mixins import JobTitleChoicesMixin
from employee.forms.forms_mixins.name_mixins import NameValidationMixin
from employee.models import Employee

COMMON_EMPLOYEE_WIDGETS = {
    "employee_name": forms.TextInput(attrs={"class": "form-control"}),
    "job_title": forms.Select(attrs={"class": "form-control"}),
    "rank": forms.Select(attrs={"class": "form-control"}),
    "money_per_hour": forms.NumberInput(
        attrs={
            "class": "form-control",
            "type": "number",
            "min": "0.01",
            "step": "0.01",
        }
    ),
}


class EmployeeForm(NameValidationMixin, JobTitleChoicesMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "employee_name",
            "department",
            "job_title",
            "rank",
            "money_per_hour",
        ]
        widgets = {
            **COMMON_EMPLOYEE_WIDGETS,
            "employee_id": forms.NumberInput(
                attrs={"class": "form-control", "type": "number", "min": "1"}
            ),
            "department": forms.Select(attrs={"class": "form-control"}),
        }


class UpdateEmployeeForm(NameValidationMixin, JobTitleChoicesMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["employee_name", "job_title", "rank", "money_per_hour"]
        widgets = {
            **COMMON_EMPLOYEE_WIDGETS,
        }
