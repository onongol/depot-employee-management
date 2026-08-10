from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class RegistrationConfirmTokenGenerator(PasswordResetTokenGenerator):
    """Signed, expiring token for registration-confirmation links.

    Subclassing (rather than reusing default_token_generator) gives this a
    distinct key_salt, so a registration-confirm token and a password-reset
    token for the same user are never interchangeable even in principle,
    and a distinct timeout setting, so tuning PASSWORD_RESET_TIMEOUT for
    password reset can't silently change how long confirmation links live.
    """

    key_salt = "employee.views.auth.tokens.RegistrationConfirmTokenGenerator"

    def check_token(self, user, token):
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return False

        if (
            self._num_seconds(self._now()) - ts
        ) > settings.REGISTRATION_CONFIRM_TIMEOUT:
            return False

        return True


registration_confirm_token_generator = RegistrationConfirmTokenGenerator()
