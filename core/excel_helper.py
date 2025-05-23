from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.styles.alignment import Alignment



def cell_builder(ws: Worksheet, row_num: int, col_num: int, content: any, styles: list[str] = []):
    cell = ws.cell(row=row_num, column=col_num)
    cell.value = content if content is not None else "-"
    for style in styles:
        if style == "rupiah" and isinstance(content, (int, float)):
            cell.number_format = '#,##0.00'
        if style == 'bold':
            cell.font = font_style(style)
        if style == "allborder":
            cell.border = Border(left=Side(style='thin'),
                                 right=Side(style='thin'),
                                 top=Side(style='thin'),
                                 bottom=Side(style='thin'))
        if style == "hborder":
            cell.border = Border(top=Side(style='thin'),
                                 bottom=Side(style='thin'))
        if style == "vborder":
            cell.border = Border(left=Side(style='thin'),
                                 right=Side(style='thin'))
    return cell


def font_style(style: str) -> Font:
    if style == "bold":
        return Font(bold=True)
    if style == "italic":
        return Font(italic=True)
    if style == "underline":
        return Font(underline="single")
    if style == "strike":
        return Font(strike=True)
    return None


def cell_border(style: str) -> Border:
    if style == "allborder":
        return Border(left=Side(style='thin'),
                      right=Side(style='thin'),
                      top=Side(style='thin'),
                      bottom=Side(style='thin'))
    elif style == "hborder":
        return Border(top=Side(style='thin'),
                      bottom=Side(style='thin'))
    elif style == "vborder":
        return Border(left=Side(style='thin'),
                      right=Side(style='thin'))

    return None

def text_align(style: str) -> Alignment:
    if style == "center":
        return Alignment(horizontal="center", vertical="center")
    if style == "left":
        return Alignment(horizontal="left", vertical="center")
    if style == "right":
        return Alignment(horizontal="right", vertical="center")
    return None