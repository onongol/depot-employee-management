def parse_month_period(
    request,
    *,
    param_name: str = "month_period",
    legacy_month: str = "legacy_month",
    legacy_year: str = "legacy_year",
):
    """
    Parse month-period from request.GET.

    Primary: ?month_period=YYYY-MM
    Legacy:  ?month=<MM>&year=<YYYY>

    Returns: (month, year, month_period)
      - month, year: int or ''
      - month_period: 'YYYY-MM' or ''
    """
    raw_month_period = (request.GET.get(param_name, "") or "").strip()

    month = year = ""
    month_period = ""

    if raw_month_period:
        try:
            y, m = raw_month_period.split("-")
            year = int(y)
            month = int(m)
            month_period = f"{year:04d}-{month:02d}"
        except ValueError:
            pass
    else:
        raw_month = request.GET.get(legacy_month, "").strip()
        raw_year = request.GET.get(legacy_year, "").strip()

        if raw_month.isdigit() and raw_year.isdigit():
            year = int(raw_year)
            month = int(raw_month)
            month_period = f"{year:04d}-{month:02d}"

    return month, year, month_period
