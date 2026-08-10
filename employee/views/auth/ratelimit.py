from django_smart_ratelimit.key_functions import get_ip_key


def ratelimit_key(scope):
    """Build a rate-limit key callable scoped to one view.

    django_smart_ratelimit's plain "ip" key maps every view onto the same
    shared bucket per IP, so two decorated views with different rates end up
    fighting over one counter. Prefixing by scope keeps them independent.
    """

    def _key(request, *args, **kwargs):
        return f"{scope}:{get_ip_key(request)}"

    return _key
