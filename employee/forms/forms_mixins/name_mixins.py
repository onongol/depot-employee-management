import re

from django import forms
from django.utils.translation import gettext_lazy as _


NAME_PATTERN = r"^[А-ЯA-ZҮӨЁ]\.[А-ЯA-ZҮӨЁ][а-яa-zёүө]*(?:-[А-ЯA-ZҮӨЁ][а-яa-zёүө-]*)*$"


class NameValidationMixin:
    """Validate 'name' field as: L.Name (e.g. D.Sukhbaatar, A.Gun-Aajav)."""

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            return name
        if not re.match(NAME_PATTERN, name):
            raise forms.ValidationError(
                _(
                    "Name must be in the format: L.Name (e.g. D.Sukhbaatar or A.Gun-Aajav)."
                )
            )
        return name
