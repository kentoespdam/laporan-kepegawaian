import pandas as pd
from icecream import ic
BULAN_LIST = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def get_nama_bulan(bulan):
    return BULAN_LIST[int(bulan) - 1]


def hitung_sisa_bulan(year: float, month: float) -> int:
    if pd.isna(year) or pd.isna(month):
        return 0
    return int(month) - int(year) * 12
