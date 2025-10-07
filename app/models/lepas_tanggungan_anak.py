import calendar
from datetime import datetime
from enum import Enum

import pandas as pd
from icecream import ic

from app.core.config import fetch_data


class FilterLepasTanggunganAnak(Enum):
    BULAN_INI = 0
    GTE_1 = 1
    GTE_2 = 2


def fetch_lepas_tanggungan_anak(
        filter: FilterLepasTanggunganAnak = FilterLepasTanggunganAnak.BULAN_INI) -> pd.DataFrame:
    """Fetch anak karyawan yang berhak menerima tunjangan lepas tanggungan"""
    now = datetime.now()
    year = now.year
    month = now.month

    if filter == FilterLepasTanggunganAnak.GTE_1:
        month += 1
    elif filter == FilterLepasTanggunganAnak.GTE_2:
        month += 2

    first_day = datetime(year, month, 1).strftime("%Y-%m-%d")
    last_day = datetime(year, month, calendar.monthrange(
        year, month)[1]).strftime("%Y-%m-%d")

    query = """
            SELECT pk.id,
                   pk.nama                                      AS nama_anak,
                   IF(pk.jenis_kelamin = 0, 'Pria', 'Wanita')   AS jenis_kelamin,
                   pk.tanggal_lahir                             AS tanggal_lahir,
                   TIMESTAMPDIFF(YEAR, pk.tanggal_lahir, now()) AS umur,
                   pk.tanggungan,
                   CASE
                       WHEN pk.status_pendidikan = 0 THEN 'Belum Sekolah'
                       WHEN pk.status_pendidikan = 1 THEN 'Sekolah'
                       ELSE 'Selesai Sekolah'
                       END                                      AS status_pendidikan,
                   bio.nama                                     AS nama_karyawan,
                   peg.nipam                                    AS nipam,
                   jab.nama                                     AS nama_jabatan
            FROM profil_keluarga AS pk
                     INNER JOIN biodata AS bio ON pk.biodata_id = bio.nik
                     INNER JOIN pegawai AS peg ON bio.nik = peg.nik
                     INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
            WHERE peg.status_kerja IN %s
              AND pk.status_kawin = %s
              AND pk.hubungan_keluarga = %s
              AND pk.tanggungan = %s
              AND (
                (DATE_ADD(pk.tanggal_lahir, INTERVAL 26 YEAR) BETWEEN %s AND %s)
                    OR (DATE_ADD(pk.tanggal_lahir, INTERVAL 21 YEAR) BETWEEN %s AND %s)
                ) \
            """
    where = ((1, 2), 0, 4, True, first_day, last_day, first_day, last_day)
    ic(query % where)

    return fetch_data(query, where)
