from django import forms

from employee.models import DailySalary

COMMON_DAILY_SALARY_WIDGETS = {
    "hours_per_day": forms.NumberInput(
        attrs={
            "class": "form-control",
            "type": "number",
            "min": "1",
            "max": "24",
        }
    ),
    "salary_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
}


class DailySalaryForm(forms.ModelForm):
    class Meta:
        model = DailySalary
        fields = ["employee", "hours_per_day", "salary_date"]
        widgets = {
            **COMMON_DAILY_SALARY_WIDGETS,
            "employee": forms.Select(attrs={"class": "form-control"}),
        }


class UpdateDailySalaryForm(forms.ModelForm):
    class Meta:
        model = DailySalary
        fields = ["hours_per_day", "salary_date"]
        widgets = {
            **COMMON_DAILY_SALARY_WIDGETS,
        }
