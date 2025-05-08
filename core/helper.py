import pandas as pd

BULAN_LIST = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]

AGAMA_LIST = [
    "Tidak Tahu",
    "Islam",
    "Kristen",
    "Katolik",
    "Hindu",
    "Budha",
    "Konghuchu",
    "Aliran Kepercayaan",
    "Lainnya",
]


def get_nama_bulan(bulan):
    return BULAN_LIST[int(bulan) - 1]


def hitung_sisa_bulan(year: float, month: float) -> int:
    if pd.isna(year) or pd.isna(month):
        return 0
    return int(month) - int(year) * 12


def get_agama(agama: int) -> str:
    if agama < 0 or agama >= len(AGAMA_LIST):
        return "Tidak Tahu"
    return AGAMA_LIST[agama]