import io
import itertools
from typing import Optional

import pandas as pd
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.worksheet.worksheet import Worksheet


def cell_builder(ws: Worksheet, row_num: int, col_num: int, content: str | int | float | None,
                 styles: Optional[list[str]]):
    """
    Build an Excel cell with given row number, column number, content, and styles

    Parameters
    ----------
    ws : Worksheet
        Excel worksheet object
    row_num : int
        row number of the cell
    col_num : int
        column number of the cell
    content : any
        content of the cell
    styles : list[str], optional
        styles of the cell, by default empty list

    Returns
    -------
    cell : openpyxl.cell.Cell
        built Excel cell object
    """
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


def font_style(style: str) -> Optional[Font]:
    if style == "bold":
        return Font(bold=True)
    if style == "italic":
        return Font(italic=True)
    if style == "underline":
        return Font(underline="single")
    if style == "strike":
        return Font(strike=True)
    return None


def cell_border(style: str) -> Optional[Border]:
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


def text_align(style: str) -> Optional[Alignment]:
    if style == "center":
        return Alignment(horizontal="center", vertical="center")
    if style == "left":
        return Alignment(horizontal="left", vertical="center")
    if style == "right":
        return Alignment(horizontal="right", vertical="center")
    return None


def write_data_to_excel(ws, data: pd.DataFrame, column_mappings: list, start_row: int) -> None:
    """Write DataFrame data to Excel worksheet"""
    row_num = itertools.count(start=start_row)

    for index, row in data.iterrows():
        current_row = next(row_num)
        col_num = itertools.count(start=1)

        for col_name, value_func, styles in column_mappings:
            value = value_func(index, row)
            cell_builder(ws, current_row, next(col_num), value, styles)


def save_workbook(wb) -> io.BytesIO:
    """Save workbook to bytes stream"""
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream
