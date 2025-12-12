from django.utils.translation import gettext_lazy as _


DELETE_BLOCK_MESSAGE = _(
    "Cannot delete %(object_name)s because it is associated with %(related)s records. "
    "Please remove the related %(related)s records first."
)
