from django import forms

from employee.models import DailySalary


class DailySalaryForm(forms.ModelForm):
    class Meta:
        model = DailySalary
        fields = "__all__"
        widgets = {
            "employee": forms.Select(attrs={"class": "form-control"}),
            "hours_per_day": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "type": "number",
                    "min": "1",
                    "max": "24",
                }
            ),
            "salary_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class UpdateDailySalaryForm(forms.ModelForm):
    class Meta:
        model = DailySalary
        fields = ["hours_per_day", "salary_date"]
        widgets = {
            "hours_per_day": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "type": "number",
                    "min": "1",
                    "max": "24",
                }
            ),
            "salary_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
