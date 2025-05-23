import io
import pandas as pd
import swifter  # noqa: F401

from core.config import LOKASI
from core.enums import get_jenis_mutasi_name
from core.model.mutasi import fetch_mutasi


def mutasi_data(from_date: str, to_date: str, jenis_mutasi: int = None) -> pd.DataFrame:
    data = fetch_mutasi(from_date, to_date, jenis_mutasi)
    if not data.empty:
        data = _cleanup(data)
    return data


def _cleanup(df: pd.DataFrame) -> pd.DataFrame:
    df["jenis_mutasi"] = df["jenis_mutasi"].swifter.apply(
        lambda x: get_jenis_mutasi_name(x))
    df["tmt_berlaku"] = df["tmt_berlaku"].swifter.apply(
        lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else None
    )
    df["lokasi"] = LOKASI

    return df


def to_excel(tahun: int, bulan: str, from_date: str, to_date: str, jenis_mutasi: int = None) -> io.BytesIO:
    data= mutasi_data(from_date, to_date, jenis_mutasi)
    if data.empty:
        return None
    
    # return io.BytesIO(data.to_excel(io.BytesIO(), index=False, columns=["Jenis Mutasi","NIK"]).getvalue())
