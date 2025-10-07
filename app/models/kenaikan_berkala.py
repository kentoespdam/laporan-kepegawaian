import calendar
from datetime import datetime
from typing import Tuple

import pandas as pd

from app.core.config import fetch_data
from app.core.enums import FilterKenaikanBerkala, JenisSk, StatusKerja, StatusPegawai


def fetch_kenaikan_berkala(filter: FilterKenaikanBerkala = FilterKenaikanBerkala.BULAN_INI) -> pd.DataFrame:
    """
    Fetch kenaikan berkala data with optimized query and date calculations.
    """
    # Build query based on filter
    builder = KenaikanBerkalaQueryBuilder()
    query, params = builder.build_query(filter)

    return fetch_data(query, params)


def _get_base_conditions() -> Tuple:
    """
    Get base SQL conditions that are common for all filters.
    """
    return (
        False,  # is_deleted
        (JenisSk.SK_KENAIKAN_PANGKAT_GOLONGAN.value, JenisSk.SK_KENAIKAN_GAJI_BERKALA.value),
        (StatusKerja.DIRUMAHKAN.value, StatusKerja.KARYAWAN_AKTIF.value),
        StatusPegawai.PEGAWAI.value
    )


def _get_date_range(filter: FilterKenaikanBerkala) -> Tuple:
    """
    Calculate date range based on filter type.
    Returns tuple of (start_date, end_date) or (year,) for year filter.
    """
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if filter == FilterKenaikanBerkala.BULAN_INI:
        # Current month
        month = current_month
        year = current_year
    elif filter == FilterKenaikanBerkala.GTE_1:
        # Next month
        month = current_month + 1
        year = current_year
        # Handle year rollover
        if month > 12:
            month = 1
            year += 1
    elif filter == FilterKenaikanBerkala.GTE_2:
        # Month after next
        month = current_month + 2
        year = current_year
        # Handle year rollover
        if month > 12:
            month = month - 12
            year += 1
    elif filter == FilterKenaikanBerkala.TAHUN_INI:
        # Current year only
        return (current_year,)
    else:
        # Default to current month
        month = current_month
        year = current_year

    # Calculate first and last day of the month
    first_day = datetime(year, month, 1).strftime("%Y-%m-%d")
    last_day = datetime(year, month, calendar.monthrange(year, month)[1]).strftime("%Y-%m-%d")

    return first_day, last_day


def _build_query_with_params(filter: FilterKenaikanBerkala, base_conditions: Tuple, date_range: Tuple) -> Tuple[
    str, Tuple]:
    """
    Build final query with parameters.
    """
    base_query = """
                 WITH ranked_sk
                          AS (SELECT ROW_NUMBER() OVER (PARTITION BY rs.pegawai_id, rs.jenis_sk ORDER BY rs.tanggal_sk DESC) AS rn,
                                     rs.id,
                                     rs.pegawai_id,
                                     peg.nipam,
                                     bio.nama,
                                     rs.jenis_sk,
                                     rs.nomor_sk,
                                     rs.tmt_berlaku,
                                     DATE_ADD(rs.tmt_berlaku, INTERVAL 4 YEAR)                                               AS tmt_kenaikan,
                                     jab.nama                                                                                AS nama_jabatan,
                                     peg.tmt_jabatan,
                                     gol.golongan,
                                     gol.pangkat,
                                     peg.tmt_golongan,
                                     TIMESTAMPDIFF(YEAR, peg.tmt_golongan, CURDATE())                                        AS mkg_tahun,
                                     TIMESTAMPDIFF(MONTH, peg.tmt_golongan, CURDATE())                                       AS mkg_bulan,
                                     peg.tmt_kerja,
                                     TIMESTAMPDIFF(YEAR, peg.tmt_kerja, CURDATE())                                           AS mk_tahun,
                                     TIMESTAMPDIFF(MONTH, peg.tmt_kerja, CURDATE())                                          AS mk_bulan,
                                     CONCAT_WS(' - ', jp.nama, pend.jurusan)                                                 AS pendidikan_terakhir,
                                     bio.tempat_lahir,
                                     bio.tanggal_lahir
                              FROM riwayat_sk rs
                                       INNER JOIN pegawai peg ON rs.pegawai_id = peg.id
                                       INNER JOIN biodata bio ON peg.nik = bio.nik
                                       INNER JOIN golongan gol ON peg.golongan_id = gol.id
                                       INNER JOIN jabatan jab ON peg.jabatan_id = jab.id
                                       INNER JOIN pendidikan pend ON pend.is_latest = TRUE AND bio.nik = pend.biodata_id
                                       INNER JOIN jenjang_pendidikan jp ON pend.jenjang_id = jp.id
                              WHERE rs.is_deleted = %s
                                AND rs.jenis_sk IN %s
                                AND peg.status_kerja IN %s
                                AND peg.status_pegawai = %s)
                 SELECT *
                 FROM ranked_sk
                 WHERE rn = 1 \
                 """

    if filter in [FilterKenaikanBerkala.BULAN_INI, FilterKenaikanBerkala.GTE_1, FilterKenaikanBerkala.GTE_2]:
        query = base_query + " AND tmt_kenaikan BETWEEN %s AND %s"
        params = base_conditions + date_range
    elif filter == FilterKenaikanBerkala.TAHUN_INI:
        query = base_query + " AND YEAR(tmt_kenaikan) = %s"
        params = base_conditions + (date_range[0],)
    else:
        query = base_query
        params = base_conditions

    return query, params


class KenaikanBerkalaQueryBuilder:
    """
    Query builder for kenaikan berkala with cached date calculations.
    """

    def __init__(self):
        self._current_date = None
        self._date_cache = {}

    def build_query(self, filter: FilterKenaikanBerkala) -> Tuple[str, Tuple]:
        """
        Build optimized query with cached date calculations.
        """
        if self._current_date != datetime.now().date():
            self._current_date = datetime.now().date()
            self._date_cache.clear()

        base_conditions = _get_base_conditions()

        if filter not in self._date_cache:
            self._date_cache[filter] = _get_date_range(filter)

        date_range = self._date_cache[filter]

        return _build_query_with_params(filter, base_conditions, date_range)
