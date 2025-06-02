from django import forms

from employee.models import Work
from employee.models import Employee


class WorkForm(forms.ModelForm):
    """Form for creating or updating a Work record."""
    # This field is used to select the department from Employee.
    department = forms.ChoiceField(
        choices=[],  # Will be set in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Department"
    )

    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'work_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.00'}),
            'standard_time': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.01'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.01'}),
        }

        error_messages = {
            'work_name': {
                'required': 'Work Name - This field is required.',
            },
            'usage_material': {
                'min_value': 'Usage of Material - Must be at least 0.00.',
            },
            'standard_time': {
                'required': 'Standard Time - This field is required.',
                'min_value': 'Standard Time - Must be at least 0.01.',
            },
            'price': {
                'required': 'Price - This field is required.',
                'min_value': 'Price - Must be at least 0.01.',
            },
        }

    # Populate the department choices dynamically from Employee model.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        departments = (
            Employee.objects.values_list('department', flat=True)
            .distinct()
        )
        self.fields['department'].choices = [(d, d) for d in departments if d]


class UpdateWorkForm(forms.ModelForm):
    """Form for updating an existing Work record."""
    class Meta:
        model = Work
        fields = ['type_material', 'usage_material', 'standard_time', 'price']
        widgets = { 
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.00'}),
            'standard_time': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.00'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0.00'}),
        }
