from typing import Optional, List, Union

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

DATE_FMT = "%d.%m.%Y"


def get_status_pegawai_vectorize(df: pd.Series):
    switcher = {
        0: "Pegawai Kontak",
        1: "Calon Pegawai",
        2: "Pegawai Tetap",
        3: "Calon Honorer Tetap",
        4: "Honorer Tetap",
        5: "Non Pegawai"
    }
    return df.map(switcher).fillna("Invalid ID")


def get_jenis_sk_vectorize(jenis_sk: pd.Series):
    switcher = {
        0: "SK Kenaikan Pangkat/Golongan",
        1: "SK Calon Pegawai",
        2: "SK Pegawai Tetap",
        3: "SK Jabatan",
        4: "SK Mutasi Lokasi Kerja",
        5: "SK Pensiun",
        6: "SK Lainnya",
        7: "SK Penyesuaian Gaji",
        8: "SK Kenaikan Gaji Berkala"
    }
    return jenis_sk.map(switcher).fillna("Invalid ID")


def get_jenis_mutasi_vectorize(jenis_mutasi: pd.Series):
    switcher = {
        0: "Pengangkatan Pertama",
        1: "Mutasi Lokasi Kerja",
        2: "Mutasi Jabatan",
        3: "Mutasi Golongan",
        4: "Mutasi Gaji",
        5: "Mutasi Gaji Berkala",
        6: "Terminasi"
    }
    return jenis_mutasi.map(switcher).fillna("Invalid ID")


def get_agama_vectorize(agama: pd.Series):
    switcher = {
        0: "Tidak Tahu",
        1: "Islam",
        2: "Kristen",
        3: "Katolik",
        4: "Hindu",
        5: "Budha",
        6: "Konghuchu",
        7: "Aliran Kepercayaan",
        8: "Lainnya",
    }
    return agama.map(switcher).fillna("Invalid ID")

def get_nama_bulan(bulan):
    return BULAN_LIST[int(bulan) - 1]


def hitung_sisa_bulan(years: pd.Series, months: pd.Series) -> pd.Series:
    try:
        years_clean = years.fillna(0).astype(int)
        months_clean = months.fillna(0).astype(int)
        result = months_clean - (years_clean * 12)
        return result.clip(lower=0)
    except (ValueError, TypeError) as e:
        # Fallback to original behavior if there are data issues
        print(f"Warning: Error in hitung_sisa_bulan: {e}")
        # Return zeros as fallback
        return pd.Series([0] * len(years), index=years.index)


def format_bulan_to_string(tanggal: pd.Series) -> str:
    tanggal=pd.to_datetime(tanggal)
    return f"{tanggal} {get_nama_bulan(tanggal.month)} {tanggal.year}"


def format_date_series(s: pd.Series, default_date: bool = False) -> pd.Series:
    """
    Convert a Series of datetimes/strings to YYYY-MM-DD strings, preserving None for invalid values.
    """
    s_dt = pd.to_datetime(s, errors="coerce")
    out = s_dt.dt.strftime(DATE_FMT)
    # Preserve None for NaT
    return out.where(s_dt.notna(), None if not default_date else "1945-08-17")


def format_date_vectorized(dates: pd.Series) -> pd.Series:
    """Vectorized date formatting"""
    if dates.empty:
        return dates

    # Convert to datetime dengan handling errors
    dates_dt = pd.to_datetime(dates, errors='coerce')

    # Mask untuk values yang valid (bukan NaT)
    valid_mask = dates_dt.notna()

    # Initialize result series dengan None
    result = pd.Series([None] * len(dates), index=dates.index)

    if valid_mask.any():
        valid_dates = dates_dt[valid_mask]

        # Vectorized operations untuk formatting
        day_str = valid_dates.dt.day.astype(str)
        year_str = valid_dates.dt.year.astype(str)
        month_names = valid_dates.dt.month.map(get_nama_bulan)

        # Combine semua components
        formatted_dates = day_str + " " + month_names + " " + year_str
        result[valid_mask] = formatted_dates

    return result


def hitung_bulan_vectorized(tahun_series: pd.Series, bulan_series: pd.Series) -> pd.Series:
    """Vectorized version of _hitung_bulan"""
    # Handle None/NA values
    tahun_clean = tahun_series.fillna(0).astype(int)
    bulan_clean = bulan_series.fillna(0).astype(int)

    # Calculate: if tahun == 0 then bulan else bulan - (tahun * 12)
    result = pd.Series([0] * len(tahun_clean), index=tahun_clean.index)

    mask_tahun_nol = tahun_clean == 0
    result[mask_tahun_nol] = bulan_clean[mask_tahun_nol]
    result[~mask_tahun_nol] = bulan_clean[~mask_tahun_nol] - (tahun_clean[~mask_tahun_nol] * 12)

    # Ensure non-negative results
    return result.clip(lower=0)


def cleanup_nan_to_zero_safe(data: Union[pd.DataFrame, pd.Series],
                             columns: Optional[List[str]] = None,
                             only_numeric: bool = True) -> Union[pd.DataFrame, pd.Series]:
    """
    Safely cleanup NaN values to zero, considering data types.

    Parameters:
    -----------
    data : pd.DataFrame or pd.Series
        Data to be cleaned
    columns : list, optional
        Specific columns to clean
    only_numeric : bool, default True
        If True, only clean numeric columns
    """
    if isinstance(data, pd.Series):
        return _cleanup_series_nan_safe(data, only_numeric)
    else:
        return _cleanup_dataframe_nan_safe(data, columns, only_numeric)


def _cleanup_series_nan_safe(series: pd.Series, only_numeric: bool = True) -> pd.Series:
    """Safely clean NaN values in Series."""
    if only_numeric and not pd.api.types.is_numeric_dtype(series):
        return series
    return series.fillna(0)


def _cleanup_dataframe_nan_safe(df: pd.DataFrame,
                                columns: Optional[List[str]] = None,
                                only_numeric: bool = True) -> pd.DataFrame:
    """Safely clean NaN values in DataFrame."""
    result = df.copy()

    if columns is None:
        columns_to_clean = result.columns
    else:
        columns_to_clean = [col for col in columns if col in result.columns]

    for col in columns_to_clean:
        if only_numeric:
            if pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(0)
        else:
            result[col] = result[col].fillna(0)

    return result