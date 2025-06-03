import io
import itertools
import swifter  # noqa: F401
import pandas as pd
from openpyxl import load_workbook

from core.excel_helper import cell_builder, font_style, text_align
from core.helper import format_bulan_to_string
from core.model.lepas_tanggungan_anak import (
    FILTER_LEPAS_TANGGUNGAN_ANAK,
    fetch_lepas_tanggungan_anak,
)


def data_lepas_tanggungan_anak(filter: FILTER_LEPAS_TANGGUNGAN_ANAK = FILTER_LEPAS_TANGGUNGAN_ANAK.BULAN_INI):
    data = fetch_lepas_tanggungan_anak(filter)
    if not data.empty:
        data = _cleanup(data)
    return data


def _cleanup(df: pd.DataFrame):
    df["tanggal_lahir"] = df["tanggal_lahir"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tanggungan"] = df["tanggungan"].swifter.apply(
        lambda x: True if x == 1 else False
    )
    return df


def to_excel(title_text: str, filter: FILTER_LEPAS_TANGGUNGAN_ANAK = FILTER_LEPAS_TANGGUNGAN_ANAK.BULAN_INI):
    result = data_lepas_tanggungan_anak(filter)
    if result.empty:
        return None

    wb = load_workbook("template/template_lta.xlsx")
    ws = wb.active

    title_cell = ws.cell(row=2, column=1)
    title_cell.value = title_text
    title_cell.alignment = text_align("center")
    title_cell.font = font_style("bold")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=9)

    row_num = itertools.count(start=5)
    for index, row in result.iterrows():
        col_num = itertools.count(start=1)
        current_row = next(row_num)
        cell_builder(ws, current_row, next(col_num),
                     int(index+1), ["bold", "allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama_anak"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["jenis_kelamin"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tanggal_lahir"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["umur"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["status_pendidikan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama_karyawan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nipam"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama_jabatan"], ["allborder"])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream
