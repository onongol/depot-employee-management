from urllib.parse import quote

import openpyxl
from django.http import HttpResponse


def export_to_excel(data, headers, filename, title):
    """
    Export given data to an Excel file.
    :param data: Iterable of rows (each row is a list or tuple)
    :param headers: List of column headers
    :param filename: Name of the Excel file to be downloaded
    :return: HttpResponse with Excel file
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = title
    ws.append(headers)
    for row in data:
        ws.append(row)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename='{quote(filename)}'"
    wb.save(response)
    return response
