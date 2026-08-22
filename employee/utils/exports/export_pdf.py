import os
import warnings
from io import BytesIO
from urllib.parse import quote

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Register font (adjust path as needed)
FONT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "fonts")
)
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# Default font name used throughout the module
FONT_NAME = "DejaVuSans"
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
else:
    warnings.warn(
        f"Font file not found: {FONT_PATH}. Falling back to built-in 'Helvetica'.",
        stacklevel=2,
    )
    FONT_NAME = "Helvetica"


def export_to_pdf(data, headers, *, col_widths, col_alignments, title, filename):
    """Export data to a PDF file with a table and custom formatting."""
    buffer = BytesIO()
    # Create a landscape A4 PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=30,
    )

    # Get default styles and set font for all styles to DejaVuSans
    styles = getSampleStyleSheet()
    for style_name in styles.byName:
        styles[style_name].fontName = FONT_NAME

    # Header paragraph style (enables wrapping)
    header_style = ParagraphStyle(
        "HeaderStyle",
        fontName=FONT_NAME,
        fontSize=10,
        leading=12,
        wordWrap="CJK",  # Enable wrapping for long headers
    )

    elements = []

    # Add the title to the PDF, centered
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["h1"],
        fontName=FONT_NAME,
        alignment=TA_CENTER,
    )

    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2 * inch))  # Add space after title

    # Define a style for table cells
    cell_style = ParagraphStyle(
        "CellStyle",
        fontName=FONT_NAME,
        fontSize=10,
        leading=12,
        wordWrap="CJK",
    )

    # Prepare table data: first row is headers, then data rows
    table_data = [[Paragraph(str(h), header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(str(cell), cell_style) for cell in row])

    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Define the base style for the table
    base_table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # Header text color
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),  # Header alignment
        ("FONTNAME", (0, 0), (-1, 0), FONT_NAME),  # Header font
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),  # Header padding
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),  # Table grid
        ("FONTNAME", (0, 1), (-1, -1), FONT_NAME),  # Body font
        ("FONTSIZE", (0, 1), (-1, -1), 10),  # Body font size
        ("LEFTPADDING", (0, 1), (-1, -1), 2),  # Body padding
        ("RIGHTPADDING", (0, 1), (-1, -1), 2),
        ("TOPPADDING", (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
    ]

    # Add custom column alignments if provided
    if col_alignments:
        base_table_style.extend(col_alignments)

    # Alternate row background color for better readability
    alternating_row_styles = [
        ("BACKGROUND", (0, i), (-1, i), colors.whitesmoke)
        for i in range(1, len(table_data))
        if i % 2 == 1
    ]

    table_style = TableStyle(base_table_style + alternating_row_styles)
    table.setStyle(table_style)
    elements.append(table)

    # Function to add page numbers to each page
    def add_page_number(canvas, doc):
        page_num_text = f"{doc.page}"
        canvas.saveState()
        canvas.setFont(FONT_NAME, 9)

        # Draw the page number at the bottom right
        canvas.drawRightString(doc.pagesize[0] - 40, 20, page_num_text)
        canvas.restoreState()

    # Build the PDF document with the elements and page number callback
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)

    # Prepare the HTTP response with the PDF file
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{quote(filename)}"'

    return response
