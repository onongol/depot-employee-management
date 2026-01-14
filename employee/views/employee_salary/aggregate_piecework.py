from django.db.models import QuerySet, Sum


def aggregate_piecework(qs: QuerySet, *, group_by_wagon: bool):
    '''Aggregate Piecework in the database (SUM) by employee and month; optionally split totals by wagon_number.'''
    values_fields = ["employee", "work_date__year", "work_date__month"]

    if group_by_wagon:
        values_fields.append("wagon_number")

    return (
        qs.values(*values_fields).annotate(
            total_piecework_amount=Sum("amount_price"),
            total_piecework_time=Sum("amount_time"),
        )
    )
