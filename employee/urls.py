from django.urls import path

from .views import home
from .views import employee_list, create_employee, update_employee,  delete_employee
from .views import work_list, create_work, update_work, delete_work
from .views import monthly_salary_list, create_monthly_salary, update_monthly_salary, delete_monthly_salary
from .views import piecework_list, create_piecework, update_piecework, delete_piecework
from .views import employee_salary_list, export_employee_salaries_excel, export_employee_salaries_pdf
from .views import calculation_materials


urlpatterns = [
    # Home URL
    path('', home, name="home"),
    # Employee URLs
    path('employee_list/', employee_list, name="employee_list"),
    path('create_employee/', create_employee, name="create_employee"),
    path('update_employee/<int:pk>/', update_employee, name="update_employee"),
    path('delete_employee/<int:pk>/', delete_employee, name="delete_employee"),
    # Work URLs
    path('work_list/', work_list, name="work_list"),
    path('create_work/', create_work, name="create_work"),
    path('update_work/<str:pk>/', update_work, name="update_work"),
    path('delete_work/<str:pk>/', delete_work, name="delete_work"),
    # MonthlySalary URLs
    path('monthly_salary_list/', monthly_salary_list, name="monthly_salary_list"),
    path('create_monthly_salary/', create_monthly_salary, name="create_monthly_salary"),
    path('update_monthly_salary/<int:pk>/', update_monthly_salary, name="update_monthly_salary"),
    path('delete_monthly_salary/<int:pk>/', delete_monthly_salary, name="delete_monthly_salary"),
    # Piecework URLs
    path('piecework_list/', piecework_list, name="piecework_list"),
    path('create_piecework/', create_piecework, name="create_piecework"),
    path('update_piecework/<int:pk>/', update_piecework, name="update_piecework"),
    path('delete_piecework/<int:pk>/', delete_piecework, name="delete_piecework"),
    # EmployeeSalary URLs
    path('employee_salary_list/', employee_salary_list, name="employee_salary_list"),
    path('export_employee_salaries_excel/', export_employee_salaries_excel, name="export_employee_salaries_excel"),
    path('export_employee_salaries_pdf/', export_employee_salaries_pdf, name="export_employee_salaries_pdf"),
    # Calculation Materials URL
    path('calculation_materials/', calculation_materials, name="calculation_materials"),
]


