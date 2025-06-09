from employee.models import Piecework


def materials_filtered(request):
    """Filtered materials data for export."""
    # Filtering (reuse logic from materials)
    selected_type = request.GET.get('type_material', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    pieceworks = (
        Piecework.objects.exclude(work__type_material__isnull=True)
        .exclude(work__type_material="Not used")
        .exclude(work__usage_material=0)
    )

    if selected_type != 'all':
        pieceworks = pieceworks.filter(work__type_material=selected_type)
    if start_date:
        pieceworks = pieceworks.filter(work_date__gte=start_date)
    if end_date:
        pieceworks = pieceworks.filter(work_date__lte=end_date)

    return pieceworks
