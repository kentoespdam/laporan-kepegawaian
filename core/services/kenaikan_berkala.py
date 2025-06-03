import io
import itertools

import pandas as pd
import swifter  # noqa: F401
from openpyxl import load_workbook

from core.enums import get_jenis_sk_name
from core.excel_helper import cell_builder, font_style, text_align
from core.helper import format_bulan_to_string
from core.model.kenaikan_berkala import FILTER_KENAIKAN_BERKALA, fetch_kenaikan_berkala


def kenaikan_berkala_data(filter: FILTER_KENAIKAN_BERKALA = FILTER_KENAIKAN_BERKALA.BULAN_INI):
    data = fetch_kenaikan_berkala(filter)
    if not data.empty:
        data = _cleanup(data)
    return data


def _cleanup(df: pd.DataFrame):
    df["tmt_berlaku"] = df["tmt_berlaku"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tmt_kenaikan"] = df["tmt_kenaikan"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tmt_jabatan"] = df["tmt_jabatan"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tmt_golongan"] = df["tmt_golongan"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tmt_kerja"] = df["tmt_kerja"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["tanggal_lahir"] = df["tanggal_lahir"].swifter.apply(
        lambda x: format_bulan_to_string(x) if x is not None else None)
    df["mkg_bulan"] = df.swifter.apply(
        lambda x: _hitung_bulan(x["mkg_tahun"], x["mkg_bulan"]), axis=1)
    df["mk_bulan"] = df.swifter.apply(
        lambda x: _hitung_bulan(x["mk_tahun"], x["mk_bulan"]), axis=1)
    df["jenis_sk"] = df["jenis_sk"].swifter.apply(
        lambda x: get_jenis_sk_name(x))
    return df


def _hitung_bulan(tahun: int, bulan: int) -> int:
    if tahun == 0:
        return bulan
    return bulan-(tahun * 12)


def to_excel(title_text: str, filter: FILTER_KENAIKAN_BERKALA):
    data = kenaikan_berkala_data(filter)
    if data.empty:
        return None

    wb = load_workbook("template/template_kenaikan_berkala.xlsx")
    ws = wb.active

    title_cell = ws.cell(row=2, column=1)
    title_cell.value = title_text
    title_cell.alignment = text_align("center")
    title_cell.font = font_style("bold")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=14)

    row_num = itertools.count(start=7)
    for index, row in data.iterrows():
        col_num = itertools.count(start=1)
        current_row = next(row_num)
        cell_builder(ws, current_row, next(col_num),
                     int(index+1), ["bold", "allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nipam"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama_jabatan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_jabatan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["pangkat"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["golongan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_golongan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mkg_tahun"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mkg_bulan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_kerja"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mk_tahun"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mk_bulan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["pendidikan_terakhir"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     "{}, {}".format(row["tempat_lahir"], row["tanggal_lahir"]), ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     "", ["allborder"])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream
