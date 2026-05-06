from django import forms

from employee.forms.forms_mixins.job_title_mixins import JobTitleChoicesMixin
from employee.forms.forms_mixins.type_wagon_mixins import TypeWagonChoicesMixin
from employee.models import Work

COMMON_WORK_WIDGETS = {
    "job_title": forms.Select(attrs={"class": "form-control"}),
    "type_wagon": forms.Select(attrs={"class": "form-control"}),
    "type_material": forms.TextInput(attrs={"class": "form-control"}),
    "usage_material": forms.NumberInput(
        attrs={
            "class": "form-control",
            "type": "number",
            "min": "0",
        }
    ),
    "standard_time": forms.NumberInput(
        attrs={
            "class": "form-control",
            "type": "number",
            "min": "0.000001",
            "step": "0.000001",
        }
    ),
    "price": forms.NumberInput(
        attrs={
            "class": "form-control",
            "type": "number",
            "min": "0.01",
            "step": "0.01",
        }
    ),
}


class WorkForm(TypeWagonChoicesMixin, JobTitleChoicesMixin, forms.ModelForm):
    class Meta:
        model = Work
        fields = [
            "work_name",
            "job_title",
            "type_wagon",
            "type_material",
            "usage_material",
            "standard_time",
            "price",
        ]
        widgets = {
            **COMMON_WORK_WIDGETS,
            "work_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class UpdateWorkForm(TypeWagonChoicesMixin, JobTitleChoicesMixin, forms.ModelForm):
    class Meta:
        model = Work
        fields = [
            "job_title",
            "type_wagon",
            "type_material",
            "usage_material",
            "standard_time",
            "price",
        ]
        widgets = {
            **COMMON_WORK_WIDGETS,
        }
