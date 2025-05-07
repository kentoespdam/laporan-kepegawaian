import io
import itertools
from openpyxl import load_workbook
from core.excel_helper import cell_builder
from core.helper import hitung_sisa_bulan
from core.model.dnp import fetch_dnp
import pandas as pd
import swifter

from core.model.organisasi import fetch_kode_nama_organisasi


def fetch_dnp_data() -> dict[str, pd.DataFrame]:
    """Fetch DNP data from database and return it in a standardized format"""
    dnp_data = fetch_dnp()
    dnp_data = _cleanup_dnp_data(dnp_data)
    organisasi = _fetch_organisasi()
    return {
        "dnp": dnp_data,
        "organisasi": organisasi
    }


def _cleanup_dnp_data(dnp_data: pd.DataFrame) -> pd.DataFrame:
    """Clean up DNP data"""
    dnp_data["mkg_tahun"] = dnp_data["mkg_tahun"].swifter.apply(
        lambda x: int(x) if x > 0 else 0)
    dnp_data["mkg_bulan"] = dnp_data.swifter.apply(
        lambda x: hitung_sisa_bulan(x["mkg_tahun"], x["mkg_bulan"]), axis=1)
    dnp_data["mk_bulan"] = dnp_data.swifter.apply(
        lambda x: hitung_sisa_bulan(x["mk_tahun"], x["mk_bulan"]), axis=1)
    dnp_data["kode_organisasi"] = dnp_data.swifter.apply(
        lambda x: _change_kode_organisasi(x), axis=1)
    return dnp_data


def _fetch_organisasi() -> pd.DataFrame:
    """Fetch and return organisasi data"""
    organisasi = fetch_kode_nama_organisasi(4)
    direksi_org = pd.DataFrame({"kode": ["1"], "nama": ["DIREKSI"]})
    organisasi = pd.concat([direksi_org, organisasi])
    return organisasi


def _change_kode_organisasi(row: pd.Series) -> str:
    """Change kode organisasi for Direksi and Direktur"""
    if row["level_jabatan"] in [2, 3, 4]:
        return "1"
    return row["kode_organisasi"]


def to_excel(tahun, bulan) -> io.BytesIO:
    df = fetch_dnp_data()
    wb = load_workbook('template/template_dnp.xlsx')
    ws = wb.active

    title_cell = ws.cell(row=2, column=1)
    title_cell.value = f"BULAN : {bulan} {tahun}"
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=16)

    root_urut = itertools.count(start=1)
    row_num = itertools.count(start=8)
    for row in df["organisasi"].itertuples():
        curr_row_num = next(row_num)
        cell_builder(ws, curr_row_num, 1, row.nama, ["bold", "vborder"])
        ws.merge_cells(start_row=curr_row_num, start_column=1,
                       end_row=curr_row_num, end_column=16)
        child_urut = itertools.count(start=1)
        for peg in find_pegawai(df["dnp"], row.kode).itertuples():
            col_num = itertools.count(start=1)
            current_row = next(row_num)
            cell_builder(ws, current_row, next(col_num),
                         next(root_urut), ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         next(child_urut), ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.nama, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.nipam, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.nama_jabatan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.tmt_jabatan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.pangkat, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.golongan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.tmt_golongan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.mkg_tahun, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.mkg_bulan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.tmt_kerja, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.mk_tahun, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.mk_bulan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.pendidikan, ["allborder"])
            cell_builder(ws, current_row, next(col_num),
                         peg.ttl, ["allborder"])
        # create empty row
        curr_row_num = next(row_num)
        cell_builder(ws, curr_row_num, 1, "", ["vborder"])
        ws.merge_cells(start_row=curr_row_num, start_column=1,
                       end_row=curr_row_num, end_column=16)

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream


def find_pegawai(df: pd.DataFrame, kode_organisasi: str) -> pd.DataFrame:
    if kode_organisasi == "1":
        return df[df["kode_organisasi"] == "1"]
    return df.query("kode_organisasi.str.startswith(@kode_organisasi)")
