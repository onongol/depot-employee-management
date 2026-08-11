from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Admin",
    "SITE_HEADER": "Administration",
    "SITE_ICON": {
        "light": lambda request: static("images/logo_light.svg"),
        "dark": lambda request: static("images/logo_dark.svg"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/x-icon",
            "href": lambda request: static("images/favicon.svg"),
        },
    ],
    "SHOW_LANGUAGES": True,
    "SIDEBAR": {
        "show_search": True,
        "command_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Administration"),
                "items": [
                    {
                        "title": _("Log entries"),
                        "link": reverse_lazy("admin:admin_logentry_changelist"),
                    },
                ],
            },
            {
                "title": _("Authentication and Authorization"),
                "items": [
                    {
                        "title": _("Groups"),
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Email"),
                        "link": reverse_lazy("admin:account_emailaddress_changelist"),
                    },
                ],
            },
            {
                "title": _("Operations"),
                "items": [
                    {
                        "title": _("Payrolls"),
                        "link": reverse_lazy("admin:employee_payroll_changelist"),
                    },
                    {
                        "title": _("Masters"),
                        "link": reverse_lazy("admin:employee_master_changelist"),
                    },
                    {
                        "title": _("Employees"),
                        "link": reverse_lazy("admin:employee_employee_changelist"),
                    },
                    {
                        "title": _("Works"),
                        "link": reverse_lazy("admin:employee_work_changelist"),
                    },
                    {
                        "title": _("Daily salaries"),
                        "link": reverse_lazy("admin:employee_dailysalary_changelist"),
                    },
                    {
                        "title": _("Daily works"),
                        "link": reverse_lazy("admin:employee_dailywork_changelist"),
                    },
                    {
                        "title": _("Pieceworks"),
                        "link": reverse_lazy("admin:employee_piecework_changelist"),
                    },
                ],
            },
        ],
    },
}
