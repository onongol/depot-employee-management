from django import forms

from employee.forms.forms_mixins.type_work_mixins import TypeWorkChoicesMixin
from employee.models import DailyWork

COMMON_DAILY_WORK_WIDGETS = {
    "type_work": forms.Select(attrs={"class": "form-control"}),
    "wagon_number": forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",
        }
    ),
    "work_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    "amount": forms.NumberInput(
        attrs={"class": "form-control", "type": "number", "min": "0.01"}
    ),
}


class DailyWorkForm(TypeWorkChoicesMixin, forms.ModelForm):
    class Meta:
        model = DailyWork
        fields = ["work", "type_work", "wagon_number", "amount", "work_date"]
        widgets = {
            **COMMON_DAILY_WORK_WIDGETS,
            "work": forms.Select(attrs={"class": "form-control"}),
        }


class UpdateDailyWorkForm(TypeWorkChoicesMixin, forms.ModelForm):
    class Meta:
        model = DailyWork
        fields = ["type_work", "wagon_number", "amount", "work_date"]
        widgets = {
            **COMMON_DAILY_WORK_WIDGETS,
        }
