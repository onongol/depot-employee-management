from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **overrides):
    """
    Build a querystring based on current request.GET and overrides.

    Usage:
      href="{% querystring group='month' page=None %}"

    Rules:
      - starts from request.GET
      - if overrides[key] is None -> remove key
      - else overrides[key] -> set/replace
      - returns "?a=1&b=2" or "" if empty
    """
    request = context.get("request")
    if request is None:
        return ""

    params = request.GET.copy()

    for key, value in overrides.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = str(value)

    qs = urlencode(params, doseq=True)
    return f"?{qs}" if qs else ""
