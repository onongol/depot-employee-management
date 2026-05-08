from employee.utils.get_value import get_value


def sum_field(rows, key: str):
    """Sum numeric field from dict/object rows, treating None as 0."""
    return sum((get_value(row, key, 0) or 0) for row in rows)
