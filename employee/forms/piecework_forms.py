from django import forms

from employee.models import Piecework


class PieceworkForm(forms.ModelForm):
    """Form for creating a new Piecework record."""
    class Meta:
        model = Piecework
        fields = '__all__'
        widgets = {
            'employee': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'work': forms.Select(attrs={'class': 'form-control'}),
            'type_work': forms.Select(attrs={'class': 'form-control'}),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }
            ),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.00'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department == 'Механик':
            self.fields['type_work'].choices = [('Депо', 'Депо')]
        else:
            self.fields['type_work'].choices = Piecework.TYPE_WORK_CHOICES
        
        

class UpdatePieceworkForm(forms.ModelForm):
    """Form for updating an existing Piecework record."""
    class Meta:
        model = Piecework
        fields = ['type_work', 'amount', 'work_date']
        widgets = {
            'type_work': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.00'
                }
            ),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department == 'Механик':
            self.fields['type_work'].choices = [('Депо', 'Депо')]
        else:
            self.fields['type_work'].choices = Piecework.TYPE_WORK_CHOICES
