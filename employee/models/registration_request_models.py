from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class RegistrationRequest(models.Model):
    """Tracks a pending self-registration until its email is confirmed."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registration_request",
    )
    register_id = models.IntegerField()
    group_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.register_id})"

    class Meta:
        verbose_name = _("Registration request")
        verbose_name_plural = _("Registration requests")
