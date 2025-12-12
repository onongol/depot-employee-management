from django.db.models import Sum


def get_total_salary_day(self, month, year):
        """Calculate total salary for the employee for a given month and year."""
        total_salary_day = self.dailysalary_set.filter(
             salary_date__month=month, 
             salary_date__year=year
        ).aggregate(total=Sum('salary_day'))['total'] or 0
        return total_salary_day


def get_total_piecework_amount(self, month, year):
    """Calculate total piecework amount for the employee for a given month and year."""
    from employee.models import Piecework   # Import only when the method is called to avoid circular imports

    total_piecework_amount = Piecework.objects.filter(
        employee=self,
        work_date__month=month,
        work_date__year=year
    ).aggregate(total=Sum('amount_price'))['total'] or 0
    return total_piecework_amount


def get_total_salary(self, month, year):
    """Calculate total salary including piecework for the employee for a given month and year."""
    total_salary_day = self.get_total_salary_day(month, year)
    total_piecework_amount = self.get_total_piecework_amount(month, year)
    total_salary = total_salary_day + total_piecework_amount
    return round(total_salary, 2)
