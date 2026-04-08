def get_content_type_label(content_type):
    """Helper function to get a human-readable label for a ContentType."""
    if not content_type:
        return ""

    model_class = content_type.model_class()
    if model_class is not None:
        return str(model_class._meta.verbose_name).title()

    return str(content_type.name).title()
