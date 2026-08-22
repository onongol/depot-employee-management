from django import forms

# Flatpickr posts "%Y-%m-%d"; the rest are formats the pages already accepted
# before the two date parsers were merged into this one list.
DATE_INPUT_FORMATS = ("%Y-%m-%d", "%Y%m%d", "%B %d, %Y", "%b %d, %Y")

# Flatpickr's range mode joins the two dates with " to "; the others are legacy.
RANGE_SEPARATORS = (" to ", " - ", "–", "—")


class FilterDateField(forms.DateField):
    """A date filter: optional, and parsed with the project-wide format list."""

    def __init__(self, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("input_formats", DATE_INPUT_FORMATS)
        super().__init__(**kwargs)


class DateRangeField(forms.Field):
    """One flatpickr range box -> (start, end). A lone date means a one-day range."""

    def __init__(self, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)
        # required=True so that a half-typed "2024-01-01 to " fails as a whole.
        self.bound = FilterDateField(required=True)

    def to_python(self, value):
        range_str = (value or "").strip()
        if not range_str:
            return None, None

        for sep in RANGE_SEPARATORS:
            if sep in range_str:
                start_str, end_str = (part.strip() for part in range_str.split(sep, 1))
                # Deliberately not reordered: a reversed range stays reversed and
                # matches nothing, which is what the list pages already did.
                return self.bound.clean(start_str), self.bound.clean(end_str)

        single = self.bound.clean(range_str)
        return single, single


class FilterForm(forms.Form):
    """Base for the GET filter forms."""

    @classmethod
    def parse(cls, data):
        """
        Return cleaned_data for the date filters.

        Unparsable input is dropped rather than reported: a typo in the box has
        to mean "this filter is not applied", never "match nothing".
        """
        form = cls(data)
        form.is_valid()
        return form.cleaned_data


class DateRangeFilterForm(FilterForm):
    """Wagon and material lists: a work-date range and nothing else."""

    range_date = DateRangeField()


class WorkDateFilterForm(DateRangeFilterForm):
    """Daily work and piecework lists."""

    record_date = FilterDateField()


class DailySalaryFilterForm(FilterForm):
    """Daily salary list."""

    salary_date = FilterDateField()
    record_date = FilterDateField()


class WorkDateForm(FilterForm):
    """The single date box on the daily work / piecework create pages."""

    work_date = FilterDateField()


class SalaryDateForm(FilterForm):
    """The single date box on the daily salary create page."""

    salary_date = FilterDateField()
