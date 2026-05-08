def parse_month_period(
    request,
    *,
    param_name: str = "month_period",
    legacy_month: str = "legacy_month",
    legacy_year: str = "legacy_year",
):
    """Parse month-period from request.GET."""
    raw_month_period = (request.GET.get(param_name, "") or "").strip()

    month = year = None
    month_period = ""

    if raw_month_period:
        try:
            raw_month, raw_year = raw_month_period.split("-")
            year_int, month_int = int(raw_year), int(raw_month)

            if 1 <= month_int <= 12 and 1900 <= year_int <= 9999:
                year, month = year_int, month_int
                month_period = f"{year:04d}-{month:02d}"

        except ValueError:
            pass
    else:
        raw_month = request.GET.get(legacy_month, "").strip()
        raw_year = request.GET.get(legacy_year, "").strip()

        if raw_month.isdigit() and raw_year.isdigit():
            year_int, month_int = int(raw_year), int(raw_month)

            if 1 <= month_int <= 12 and 1900 <= year_int <= 9999:
                year, month = year_int, month_int
                month_period = f"{year:04d}-{month:02d}"

    return month, year, month_period
