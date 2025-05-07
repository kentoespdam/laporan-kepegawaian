from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font


def cell_builder(ws: Worksheet, row_num: int, col_num: int, content: any, styles: list[str]=[]):
    cell = ws.cell(row=row_num, column=col_num)
    cell.value = content if content is not None else "-"
    for style in styles:
        if style == "rupiah" and isinstance(content, (int, float)):
            cell.number_format = '#,##0.00'
        if style == 'bold':
            cell.font = Font(bold=True)
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
