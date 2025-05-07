import io
import itertools
from openpyxl import load_workbook
from core.enums import get_status_pegawai_name
from core.excel_helper import cell_builder
import pandas as pd
from core.helper import hitung_sisa_bulan
from core.model.duk import fetch_duk
import io
import swifter


def duk_data():
    data = fetch_duk()
    data = cleanup(data)
    return data


def cleanup(df: pd.DataFrame) -> pd.DataFrame:
    df["tmt_golongan"] = df["tmt_golongan"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["tmt_jabatan"] = df["tmt_jabatan"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["tmt_kerja"] = df["tmt_kerja"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["mk_bulan"] = df.swifter.apply(
        lambda x: hitung_sisa_bulan(x["mk_tahun"], x["mk_bulan"]), axis=1)
    df["status_pegawai"] = df["status_pegawai"].swifter.apply(
        lambda x: get_status_pegawai_name(x))
    return df


def to_excel(tahun, bulan) -> io.BytesIO:
    data = duk_data()
    wb = load_workbook('template/template_duk.xlsx')
    ws = wb.active

    title_cell = ws.cell(row=2, column=1)
    title_cell.value = f"BULAN : {bulan} {tahun}"
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=16)

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
                     row["golongan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["pangkat"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_golongan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["nama_jabatan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_jabatan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tmt_kerja"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mk_tahun"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["mk_bulan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["jurusan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tahun_lulus"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["tingkat_pendidikan"], ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     int(row["usia"]),  ["allborder"])
        cell_builder(ws, current_row, next(col_num),
                     row["status_pegawai"], ["allborder"])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream
