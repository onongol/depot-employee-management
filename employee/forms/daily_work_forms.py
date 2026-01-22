from django import forms

from employee.forms.forms_mixins.type_work_mixins import TypeWorkChoiceMixin
from employee.models import DailyWork


class DailyWorkForm(TypeWorkChoiceMixin, forms.ModelForm):
    class Meta:
        model = DailyWork
        fields = "__all__"
        widgets = {
            "work": forms.Select(attrs={"class": "form-control"}),
            "type_work": forms.Select(attrs={"class": "form-control"}),
            "wagon_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                }
            ),
            "work_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "type": "number", "min": "0.01"}
            ),
        }


class UpdateDailyWorkForm(TypeWorkChoiceMixin, forms.ModelForm):
    class Meta:
        model = DailyWork
        fields = ["type_work", "wagon_number", "amount", "work_date"]
        widgets = {
            "type_work": forms.Select(attrs={"class": "form-control"}),
            "wagon_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                }
            ),
            "work_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "type": "number", "min": "0.01"}
            ),
        }
