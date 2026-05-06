import re

from django import forms
from django.utils.translation import gettext_lazy as _

NAME_PATTERN = re.compile(
    r"^[А-ЯA-ZҮӨЁ]\.[А-ЯA-ZҮӨЁ][а-яa-zёүө]*(?:-[А-ЯA-ZҮӨЁ][а-яa-zёүө-]*)*$"
)


class NameValidationMixin:
    def clean_employee_name(self):
        name = self.cleaned_data.get("employee_name")
        if not name:
            return name
        if not NAME_PATTERN.match(name):
            raise forms.ValidationError(_("Format: Surname.Name (e.g. R.Choinom)."))
        return name
