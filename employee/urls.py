from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from django_smart_ratelimit import rate_limit

from employee.forms.login_forms import CustomAuthenticationForm
from employee.forms.password_reset_forms import (
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from employee.views.auth.confirm_views import (
    register_confirm_view,
    register_resend_view,
)
from employee.views.auth.password_views import CustomPasswordChangeView
from employee.views.auth.ratelimit import ratelimit_key
from employee.views.auth.register_views import register_done_view, register_view
from employee.views.daily_salary import (
    DailySalaryUpdateView,
    daily_salary_create,
    daily_salary_delete_bulk,
    daily_salary_list,
)
from employee.views.daily_work import (
    DailyWorkUpdateView,
    daily_work_create,
    daily_work_delete_bulk,
    daily_work_export_excel,
    daily_work_list,
)
from employee.views.department import set_department
from employee.views.employee import (
    EmployeeCreateView,
    EmployeeUpdateView,
    employee_activate,
    employee_deactivate,
    employee_delete_bulk,
    employee_list,
)
from employee.views.employee_salary import (
    employee_salary_export_excel,
    employee_salary_export_pdf,
    employee_salary_list,
)
from employee.views.home import home
from employee.views.material import material_export_excel, material_list
from employee.views.piecework import (
    PieceworkUpdateView,
    piecework_create,
    piecework_export_excel,
    piecework_list,
)
from employee.views.wagon import wagon_export_excel, wagon_list
from employee.views.work import (
    WorkCreateView,
    WorkUpdateView,
    work_delete_bulk,
    work_list,
)

urlpatterns = [
    # Home URL
    path("", home, name="home"),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="auth/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path("register/", register_view, name="register"),
    path("register/done/", register_done_view, name="register_done"),
    path(
        "register/confirm/<uidb64>/<token>/",
        register_confirm_view,
        name="register_confirm",
    ),
    path("register/resend/", register_resend_view, name="register_resend"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    # Password change URLs
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    # Password reset URLs
    path(
        "password_reset/",
        rate_limit(key=ratelimit_key("password_reset"), rate="5/h")(
            auth_views.PasswordResetView.as_view(
                template_name="auth/password_reset_form.html",
                email_template_name="auth/email/password_reset_email.txt",
                subject_template_name="auth/email/password_reset_subject.txt",
                form_class=CustomPasswordResetForm,
                success_url=reverse_lazy("password_reset_done"),
            )
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Department URLs
    path("set_department/", set_department, name="set_department"),
    # Employee URLs
    path("employee/", employee_list, name="employee_list"),
    path("employee_create/", EmployeeCreateView.as_view(), name="employee_create"),
    path(
        "employee_update/<int:pk>/",
        EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path("employee_delete_bulk/", employee_delete_bulk, name="employee_delete_bulk"),
    # Employee activation/deactivation
    path(
        "employee/<int:pk>/deactivate/", employee_deactivate, name="employee_deactivate"
    ),
    path("employee/<int:pk>/activate/", employee_activate, name="employee_activate"),
    # Work URLs
    path("work/", work_list, name="work_list"),
    path("work_create/", WorkCreateView.as_view(), name="work_create"),
    path("work_update/<str:pk>/", WorkUpdateView.as_view(), name="work_update"),
    path("work_delete_bulk/", work_delete_bulk, name="work_delete_bulk"),
    # DailySalary URLs
    path("daily_salary/", daily_salary_list, name="daily_salary_list"),
    path("daily_salary_create/", daily_salary_create, name="daily_salary_create"),
    path(
        "daily_salary_update/<int:pk>/",
        DailySalaryUpdateView.as_view(),
        name="daily_salary_update",
    ),
    path(
        "daily_salary_delete_bulk/",
        daily_salary_delete_bulk,
        name="daily_salary_delete_bulk",
    ),
    # Daily Work URLs
    path("daily_work/", daily_work_list, name="daily_work_list"),
    path("daily_work_create/", daily_work_create, name="daily_work_create"),
    path(
        "daily_work_update/<int:pk>/",
        DailyWorkUpdateView.as_view(),
        name="daily_work_update",
    ),
    path(
        "daily_work_export_excel/",
        daily_work_export_excel,
        name="daily_work_export_excel",
    ),
    path(
        "daily_work_delete_bulk/", daily_work_delete_bulk, name="daily_work_delete_bulk"
    ),
    # Piecework URLs
    path("piecework/", piecework_list, name="piecework_list"),
    path("piecework_create/", piecework_create, name="piecework_create"),
    path(
        "piecework_update/<int:pk>/",
        PieceworkUpdateView.as_view(),
        name="piecework_update",
    ),
    path(
        "piecework_export_excel/", piecework_export_excel, name="piecework_export_excel"
    ),
    # EmployeeSalary URLs
    path("employee_salary/", employee_salary_list, name="employee_salary_list"),
    path(
        "employee_salary_export_excel/",
        employee_salary_export_excel,
        name="employee_salary_export_excel",
    ),
    path(
        "employee_salary_export_pdf/",
        employee_salary_export_pdf,
        name="employee_salary_export_pdf",
    ),
    # Wagon URLs
    path("wagon/", wagon_list, name="wagon_list"),
    path("wagon_export_excel/", wagon_export_excel, name="wagon_export_excel"),
    # Materials URLs
    path("material/", material_list, name="material_list"),
    path("material_export_excel/", material_export_excel, name="material_export_excel"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
