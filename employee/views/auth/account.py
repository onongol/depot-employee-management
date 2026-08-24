from allauth.mfa.utils import is_mfa_enabled
from allauth.usersessions.models import UserSession
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def account_overview(request):
    context = {
        "is_mfa_enabled": is_mfa_enabled(request.user),
        "session_count": len(UserSession.objects.purge_and_list(request.user)),
    }
    return render(request, "account/overview.html", context)
