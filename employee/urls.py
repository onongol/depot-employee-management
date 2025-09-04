from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views.home import home
from .views.auth.register_views import register_view
from .views.auth.password_views import CustomPasswordChangeView
from .views.department import set_department
from .views.employee import employee_list, employee_activate, employee_deactivate
from .views.employee import EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView
from .views.work import work_list
from .views.work import WorkCreateView, WorkUpdateView, WorkDeleteView
from .views.daily_salary import daily_salary_list, daily_salary_create
from .views.daily_salary import DailySalaryUpdateView, DailySalaryDeleteView
from .views.piecework import piecework_list, piecework_create
from .views.piecework import PieceworkUpdateView, PieceworkDeleteView
from .views.employee_salary import employee_salary_list, employee_salary_export_excel, employee_salary_export_pdf
from .views.materials import materials, export_materials_excel

from .views.wagon.wagon_views import wagon_list


urlpatterns = [
    # Home URL
    path('', home, name="home"),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Password change URLs
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    # Department URLs
    path('set_department/', set_department, name="set_department"),
    # Employee URLs
    path('employee_list/', employee_list, name="employee_list"),
    path('employee_create/', EmployeeCreateView.as_view(), name="employee_create"),
    path('employee_update/<int:pk>/', EmployeeUpdateView.as_view(), name="employee_update"),
    path('employee_delete/<int:pk>/', EmployeeDeleteView.as_view(), name="employee_delete"),
    # Employee activation/deactivation
    path('employee/<int:pk>/deactivate/', employee_deactivate, name='employee_deactivate'),
    path('employee/<int:pk>/activate/', employee_activate, name='employee_activate'),
    # Work URLs
    path('work_list/', work_list, name="work_list"),
    path('work_create/', WorkCreateView.as_view(), name="work_create"),
    path('work_update/<str:pk>/', WorkUpdateView.as_view(), name="work_update"),
    path('work_delete/<str:pk>/', WorkDeleteView.as_view(), name="work_delete"),
    # DailySalary URLs
    path('daily_salary_list/', daily_salary_list, name="daily_salary_list"),
    path('daily_salary_create/', daily_salary_create, name="daily_salary_create"),
    path('daily_salary_update/<int:pk>/', DailySalaryUpdateView.as_view(), name="daily_salary_update"),
    path('daily_salary_delete/<int:pk>/', DailySalaryDeleteView.as_view(), name="daily_salary_delete"),
    # Piecework URLs
    path('piecework_list/', piecework_list, name="piecework_list"),
    path('piecework_create/', piecework_create, name="piecework_create"),
    path('piecework_update/<int:pk>/', PieceworkUpdateView.as_view(), name="piecework_update"),
    path('piecework_delete/<int:pk>/', PieceworkDeleteView.as_view(), name="piecework_delete"),
    # EmployeeSalary URLs
    path('employee_salary_list/', employee_salary_list, name="employee_salary_list"),
    path('employee_salary_export_excel/', employee_salary_export_excel, name="employee_salary_export_excel"),
    path('employee_salary_export_pdf/', employee_salary_export_pdf, name="employee_salary_export_pdf"),
    # Wagon URLs
    path('wagon_list/', wagon_list, name="wagon_list"),
    # Materials URL
    path('materials/', materials, name="materials"),
    path('export_materials_excel/', export_materials_excel, name="export_materials_excel"),
]

if settings.DEBUG:
    urlpatterns += [
        # Include Django Browser Reload URLs for development
        path('__reload__/', include('django_browser_reload.urls')),
    ]
