from django import forms
from django.utils.translation import gettext_lazy as _

from employee.forms.forms_mixins.type_wagon_mixins import TypeWagonChoicesMixin
from employee.forms.forms_mixins.work_job_titel_mixins import JobTitleChoicesMixin
from employee.forms.forms_mixins.work_mixins import WorkNameUniqueMixin
from employee.models import Work


class WorkForm(
    TypeWagonChoicesMixin, JobTitleChoicesMixin, WorkNameUniqueMixin, forms.ModelForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Work
        fields = "__all__"
        widgets = {
            "job_title": forms.Select(attrs={"class": "form-control"}),
            "work_name": forms.TextInput(attrs={"class": "form-control"}),
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


class UpdateWorkForm(
    TypeWagonChoicesMixin, JobTitleChoicesMixin, WorkNameUniqueMixin, forms.ModelForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    "min": "0",
                    "step": "0.000001",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "type": "number",
                    "min": "0",
                    "step": "0.01",
                }
            ),
        }
