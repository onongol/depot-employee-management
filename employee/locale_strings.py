"""Translation-only strings used by validators and tooling.

This module lists strings wrapped with ``gettext_noop`` so they are
discovered by Django's translation extraction (``makemessages``).
These strings may be referenced only by validators or external libraries
and therefore might not appear in templates or other scanned code paths.

Import this module at app startup (for example in
``EmployeeConfig.ready()``) if you need to ensure the module is
loaded during runtime. Using ``gettext_noop`` marks the strings for
extraction but does not perform translation at import time.
"""

from django.utils.translation import gettext_noop

gettext_noop("Your password can’t be too similar to your other personal information.")
gettext_noop("Your password can’t be a commonly used password.")
gettext_noop("Your password can’t be entirely numeric.")
gettext_noop("The two password fields didn’t match.")
