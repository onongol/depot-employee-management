from django import forms

from employee.forms.forms_mixins.type_work_mixins import TypeWorkChoicesMixin
from employee.models import Piecework

COMMON_PIECEWORK_WIDGETS = {
    "type_work": forms.Select(attrs={"class": "form-control"}),
    "work_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    "amount": forms.NumberInput(
        attrs={"class": "form-control", "type": "number", "min": "0.01"}
    ),
}


class PieceworkForm(TypeWorkChoicesMixin, forms.ModelForm):
    class Meta:
        model = Piecework
        fields = [
            "employee",
            "work",
            "type_work",
            "wagon_number",
            "amount",
            "work_date",
        ]
        widgets = {
            **COMMON_PIECEWORK_WIDGETS,
            "employee": forms.Select(attrs={"class": "form-control"}),
            "work": forms.Select(attrs={"class": "form-control"}),
        }


class UpdatePieceworkForm(TypeWorkChoicesMixin, forms.ModelForm):
    class Meta:
        model = Piecework
        fields = ["type_work", "wagon_number", "amount", "work_date"]
        widgets = {
            **COMMON_PIECEWORK_WIDGETS,
        }
