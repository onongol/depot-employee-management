from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


def get_content_type_label(content_type: ContentType | None) -> str:
    """Return a human-readable label for a ContentType."""
    if not content_type:
        return _("Unknown model")

    model_class = content_type.model_class()
    if model_class is not None:
        return str(model_class._meta.verbose_name)

    return str(content_type.name or _("Unknown model"))
