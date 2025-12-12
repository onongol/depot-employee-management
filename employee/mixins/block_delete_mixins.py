from django.utils.translation import gettext_lazy as _

from employee.messages.delete_block import DELETE_BLOCK_MESSAGE


class BlockDeleteMixin:
    """
    Provides a generic get_block_message based on a list of related record labels.
    Views can set block_related_models = ['Daily Salary', 'Piecework'].
    """
    block_related_models: tuple[str, ...] = ()

    def get_block_message(self):
        if not self.block_related_models:
            return ''
        
        related = ', '.join(str(_(label)) for label in self.block_related_models)
        return DELETE_BLOCK_MESSAGE % {
            'object_name': self.get_object_name(),
            'related': related
        }
