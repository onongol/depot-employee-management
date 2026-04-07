from django.contrib import admin


def make_logentry_display(attr_name, title):
    @admin.display(description=title)
    def _display(self, obj):
        return getattr(obj, attr_name)

    return _display
