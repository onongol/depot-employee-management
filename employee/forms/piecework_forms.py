from django import forms

from employee.forms.forms_mixins.type_work_mixins import TypeWorkChoiceMixin
from employee.models import Piecework


class PieceworkForm(TypeWorkChoiceMixin, forms.ModelForm):
    class Meta:
        model = Piecework
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
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
                'min': '0.01'
                }
            ),
        }        
        

class UpdatePieceworkForm(TypeWorkChoiceMixin, forms.ModelForm):
    class Meta:
        model = Piecework
        fields = ['type_work', 'wagon_number', 'amount', 'work_date']
        widgets = {
            'type_work': forms.Select(attrs={'class': 'form-control'}),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }
            ),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.01'
                }
            ),  
        }
