from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from io import BytesIO

# Register font (adjust path as needed)
FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts')
FONT_PATH = os.path.join(FONT_DIR, 'DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans', FONT_PATH))


def export_to_pdf(data, headers, col_widths, col_alignments, title, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    for style_name in styles.byName:
        styles[style_name].fontName = 'DejaVuSans'

    elements = []
    title_style = styles['h1']
    title_style.alignment = TA_CENTER
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2 * inch))

    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='DejaVuSans',
        fontSize=10,
        leading=12,
        wordWrap='CJK',
    )

    table_data = [headers]
    for row in data:
        table_data.append([
            Paragraph(cell, cell_style) if isinstance(cell, str) else str(cell)
            for cell in row
        ])

    table = Table(table_data, colWidths=col_widths)

    base_table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 1), (-1, -1), 2),
        ('RIGHTPADDING', (0, 1), (-1, -1), 2),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
    ]
    if col_alignments:
        base_table_style.extend(col_alignments)
    alternating_row_styles = [
        ('BACKGROUND', (0, i), (-1, i), colors.whitesmoke)
        for i in range(1, len(table_data)) if i % 2 == 1
    ]
    table_style = TableStyle(base_table_style + alternating_row_styles)
    table.setStyle(table_style)
    elements.append(table)

    def add_page_number(canvas, doc):
        page_num_text = f"{doc.page}"
        canvas.saveState()
        canvas.setFont('DejaVuSans', 9)
        canvas.drawRightString(
            doc.pagesize[0] - 40,
            20,
            page_num_text
        )
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
