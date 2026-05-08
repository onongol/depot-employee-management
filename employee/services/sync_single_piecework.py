def sync_single_piecework(piecework, dailywork, salary_map):
    """Sync a single Piecework with its DailyWork and recalculate amount_price."""
    from employee.services.calculate_piecework_update import calculate_piecework_update
    from employee.services.daily_work_calculations import calculate_time_amount

    piecework.job_title = dailywork.job_title
    piecework.type_work = dailywork.type_work
    piecework.type_wagon = dailywork.type_wagon
    piecework.wagon_number = dailywork.wagon_number
    piecework.amount = dailywork.amount
    piecework.work_date = dailywork.work_date
    piecework.work_year = dailywork.work_year
    piecework.work_month = dailywork.work_month

    piecework.amount_time = calculate_time_amount(dailywork.work, piecework.amount)

    daily_salary = salary_map.get(piecework.employee_id)

    piecework.amount_price = calculate_piecework_update(
        dailywork.work, piecework.amount, daily_salary, salary_map.values()
    )

    piecework.save(
        update_fields=[
            "job_title",
            "type_work",
            "type_wagon",
            "wagon_number",
            "amount",
            "amount_time",
            "amount_price",
            "work_date",
            "work_year",
            "work_month",
        ]
    )
