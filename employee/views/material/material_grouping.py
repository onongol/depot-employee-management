from django.db.models import Sum


def group_and_sum_materials(queryset):
    """Group and sum duplicate materials by date, work name, and material type."""
    
    return (
        queryset.values("work_date", "work__work_name", "work__type_material")
        .annotate(amount_material=Sum("amount_material"))
        .order_by("-work_date", "work__work_name", "work__type_material")
    )
