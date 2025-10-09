from enum import Enum

import pandas as pd

from app.core.config import fetch_data
from app.core.enums import StatusKerja, StatusPegawai


class FilterKontrak(Enum):
    AKTIF = 0
    THIS_MONTH = 1
    GTE_1_MONTH = 2
    GTE_2_MONTH = 3
    GTE_3_MONTH = 4
    ENDED = 5


def fetch_kontrak(filter: FilterKontrak = FilterKontrak.AKTIF) -> pd.DataFrame:
    sql = """
          SELECT peg.nipam,
                 bio.nama,
                 rk.nomor_kontrak,
                 organisasi.nama                                 AS nama_organisasi,
                 jabatan.nama                                    AS nama_jabatan,
                 rk.tanggal_mulai,
                 rk.tanggal_selesai,
                 TIMESTAMPDIFF(YEAR, now(), rk.tanggal_selesai)  AS sisa_tahun,
                 TIMESTAMPDIFF(MONTH, now(), rk.tanggal_selesai) AS sisa_bulan
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
                   LEFT JOIN riwayat_kontrak AS rk ON peg.id = rk.pegawai_id
              AND rk.is_latest = TRUE
                   INNER JOIN organisasi ON peg.organisasi_id = organisasi.id
                   INNER JOIN jabatan ON peg.jabatan_id = jabatan.id
          WHERE rk.nomor_kontrak IS NOT NULL
            AND peg.status_pegawai = %s \
          """
    where = (StatusPegawai.KONTRAK.value,)
    if filter == FilterKontrak.THIS_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())
        """
        where += (StatusKerja.KARYAWAN_AKTIF.value,)
    elif filter == FilterKontrak.GTE_1_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+1
        """
        where += (StatusKerja.KARYAWAN_AKTIF.value,)
    elif filter == FilterKontrak.GTE_2_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+2
        """
        where += (StatusKerja.KARYAWAN_AKTIF.value,)
    elif filter == FilterKontrak.GTE_3_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+3
        """
        where += (StatusKerja.KARYAWAN_AKTIF.value,)
    elif filter == FilterKontrak.ENDED:
        sql += """
            AND peg.status_kerja IN %s
        """
        where += (tuple([StatusKerja.DIRUMAHKAN.value, StatusKerja.BERHENTI_OR_KELUAR.value]),)
    else:
        sql += """
            AND peg.status_kerja = %s
            AND rk.tanggal_selesai >= CURDATE()
        """
        where += (StatusKerja.KARYAWAN_AKTIF.value,)

    return fetch_data(sql, where)
