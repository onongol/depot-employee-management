from allauth.usersessions.models import UserSession
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST


@require_POST
@login_required
def end_user_session(request, session_id):
    session = get_object_or_404(UserSession, pk=session_id, user=request.user)
    if not session.is_current():
        session.end()
        messages.success(request, _("Session signed out."))
    return redirect(reverse("usersessions_list"))
