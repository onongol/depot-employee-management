from employee.constants.constants import GROUP_MONTH, GROUP_YEAR


def is_detail_group(group):
    return group not in (GROUP_MONTH, GROUP_YEAR)


def is_grouped(group):
    return group in (GROUP_MONTH, GROUP_YEAR)


def is_month_group(group):
    return group == GROUP_MONTH


def is_year_group(group):
    return group == GROUP_YEAR
