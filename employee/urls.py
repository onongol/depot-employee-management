from django.urls import path

from .views.home import home
from .views.department import set_department
from .views.employee import employee_list, employee_create, employee_update, employee_delete
from .views.work import work_list, work_create, work_update, work_delete
from .views.daily_salary import daily_salary_list, daily_salary_create, daily_salary_update, daily_salary_delete
from .views.piecework import piecework_list, piecework_create, piecework_update, piecework_delete
from .views.employee_salary import employee_salary_list, employee_salary_export_excel, employee_salary_export_pdf
from .views.materials import materials, export_materials_excel


urlpatterns = [
    # Home URL
    path('', home, name="home"),
    # Department URLs
    path('set_department/', set_department, name="set_department"),
    # Employee URLs
    path('employee_list/', employee_list, name="employee_list"),
    path('employee_create/', employee_create, name="employee_create"),
    path('employee_update/<int:pk>/', employee_update, name="employee_update"),
    path('employee_delete/<int:pk>/', employee_delete, name="employee_delete"),
    # Work URLs
    path('work_list/', work_list, name="work_list"),
    path('work_create/', work_create, name="work_create"),
    path('work_update/<str:pk>/', work_update, name="work_update"),
    path('work_delete/<str:pk>/', work_delete, name="work_delete"),
    # DailySalary URLs
    path('daily_salary_list/', daily_salary_list, name="daily_salary_list"),
    path('daily_salary_create/', daily_salary_create, name="daily_salary_create"),
    path('daily_salary_update/<int:pk>/', daily_salary_update, name="daily_salary_update"),
    path('daily_salary_delete/<int:pk>/', daily_salary_delete, name="daily_salary_delete"),
    # Piecework URLs
    path('piecework_list/', piecework_list, name="piecework_list"),
    path('piecework_create/', piecework_create, name="piecework_create"),
    path('piecework_update/<int:pk>/', piecework_update, name="piecework_update"),
    path('piecework_delete/<int:pk>/', piecework_delete, name="piecework_delete"),
    # EmployeeSalary URLs
    path('employee_salary_list/', employee_salary_list, name="employee_salary_list"),
    path('employee_salary_export_excel/', employee_salary_export_excel, name="employee_salary_export_excel"),
    path('employee_salary_export_pdf/', employee_salary_export_pdf, name="employee_salary_export_pdf"),
    # Materials URL
    path('materials/', materials, name="materials"),
    path('export_materials_excel/', export_materials_excel, name="export_materials_excel"),
]
