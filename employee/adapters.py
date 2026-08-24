from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """Once MFA is set up, reauthentication requires a fresh code instead of just the password (OWASP MFA guidance)."""

    def get_reauthentication_methods(self, user):
        methods = super().get_reauthentication_methods(user)
        mfa_methods = [m for m in methods if m["id"] == "mfa_reauthenticate"]
        return mfa_methods or methods
