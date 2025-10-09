from datetime import datetime
from enum import Enum
from typing import Tuple

import pandas as pd
from markdown_it.parser_block import LOGGER

from app.core.config import fetch_data
from app.core.enums import HubunganKeluarga, StatusKerja, StatusPendidikan


class FilterLepasTanggunganAnak(Enum):
    BULAN_INI = 0
    GTE_1 = 1
    GTE_2 = 2


def fetch_lepas_tanggungan_anak(
        filter_type: FilterLepasTanggunganAnak = FilterLepasTanggunganAnak.BULAN_INI) -> pd.DataFrame:
    """Fetch anak karyawan dengan perhitungan umur berdasarkan tanggal referensi bulan ini."""

    target_month, target_year = _get_target_month_year(filter_type)
    min_umur, max_umur = 21, 26

    # Query yang lebih sederhana dengan DATE_FORMAT untuk perhitungan umur konsisten
    query = """
            SELECT pk.id,
                   pk.nama                                      AS nama_anak,
                   IF(pk.jenis_kelamin = 0, 'Pria', 'Wanita')   AS jenis_kelamin,
                   pk.tanggal_lahir,
                   TIMESTAMPDIFF(YEAR, pk.tanggal_lahir, NOW()) AS umur,
                   pk.tanggungan,
                   CASE pk.status_pendidikan
                       WHEN 0 THEN 'Belum Sekolah'
                       WHEN 1 THEN 'Sekolah'
                       ELSE 'Selesai Sekolah'
                       END                                      AS status_pendidikan,
                   bio.nama                                     AS nama_karyawan,
                   peg.nipam                                    AS nipam,
                   jab.nama                                     AS nama_jabatan
            FROM profil_keluarga pk
                     INNER JOIN biodata bio
                                ON pk.biodata_id = bio.nik
                     INNER JOIN pegawai peg ON bio.nik = peg.nik AND peg.is_deleted = FALSE
                     INNER JOIN jabatan jab ON peg.jabatan_id = jab.id
            WHERE peg.status_kerja IN (%s, %s)
              AND pk.hubungan_keluarga = %s
              AND pk.status_pendidikan != %s
              AND MONTH(pk.tanggal_lahir) = %s
              AND TIMESTAMPDIFF(YEAR
                , pk.tanggal_lahir
                , STR_TO_DATE(CONCAT(%s, '-', %s, '-15'), '%%Y-%%m-%%d')
                  ) BETWEEN %s
                AND %s
            """

    params = (
        StatusKerja.DIRUMAHKAN.value,
        StatusKerja.KARYAWAN_AKTIF.value,
        HubunganKeluarga.ANAK.value,
        StatusPendidikan.SELESAI_SEKOLAH.value,
        target_month,  # filter bulan lahir
        target_year, target_month,  # untuk perhitungan umur
        min_umur,
        max_umur
    )

    try:
        result = fetch_data(query, params)
        return result
    except Exception as e:
        LOGGER.error(f"Error fetching data: {e}")
        return pd.DataFrame()


def _get_target_month_year(filter_type: FilterLepasTanggunganAnak) -> Tuple[int, int]:
    """Get target month dan year dengan handling year rollover yang lebih robust."""
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    adjustment = filter_type.value

    # Calculate target month and year
    total_months = current_month + adjustment
    target_year = current_year + (total_months - 1) // 12
    target_month = (total_months - 1) % 12 + 1

    return target_month, target_year
