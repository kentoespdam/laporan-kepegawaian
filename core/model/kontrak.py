from enum import Enum
import pandas as pd
from core.config import get_connection_pool
from core.enums import STATUS_KERJA, STATUS_PEGAWAI
from icecream import ic

class FILTER_KONTRAK(Enum):
    AKTIF = 0
    THIS_MONTH = 1
    GTE_1_MONTH = 2
    GTE_2_MONTH = 3
    GTE_3_MONTH = 4
    ENDED = 5


def fetch_kontrak(filter: FILTER_KONTRAK = FILTER_KONTRAK.AKTIF) -> pd.DataFrame:
    sql = """
        SELECT
            peg.nipam,
            bio.nama,
            rk.nomor_kontrak,
            organisasi.nama AS nama_organisasi,
            jabatan.nama AS nama_jabatan,
            rk.tanggal_mulai,
            rk.tanggal_selesai,
            TIMESTAMPDIFF( YEAR, now(), rk.tanggal_selesai ) AS sisa_tahun,
            TIMESTAMPDIFF( MONTH, now(), rk.tanggal_selesai ) AS sisa_bulan 
        FROM
            pegawai AS peg
        INNER JOIN biodata AS bio ON peg.nik = bio.nik
        LEFT JOIN riwayat_kontrak AS rk ON peg.id = rk.pegawai_id 
            AND rk.is_latest =TRUE 
        INNER JOIN organisasi ON peg.organisasi_id = organisasi.id
        INNER JOIN jabatan ON peg.jabatan_id = jabatan.id 
        WHERE
            rk.nomor_kontrak IS NOT NULL
            AND peg.status_pegawai = %s
    """
    where = (STATUS_PEGAWAI.KONTRAK.value, STATUS_KERJA.KARYAWAN_AKTIF.value)
    if filter == FILTER_KONTRAK.THIS_MONTH:
        sql += """ 
            AND peg.status_kerja = %s 
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())
        """
    elif filter == FILTER_KONTRAK.GTE_1_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+1
        """
    elif filter == FILTER_KONTRAK.GTE_2_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+2
        """
    elif filter == FILTER_KONTRAK.GTE_3_MONTH:
        sql += """
            AND peg.status_kerja = %s
            AND YEAR(rk.tanggal_selesai)=YEAR(CURDATE())
            AND MONTH(rk.tanggal_selesai)=MONTH(CURDATE())+3
        """
    elif filter == FILTER_KONTRAK.ENDED:
        sql += """
            AND peg.status_kerja IN %s
        """
        where = (STATUS_PEGAWAI.KONTRAK.value,
                 (STATUS_KERJA.DIRUMAHKAN.value, STATUS_KERJA.BERHENTI_OR_KELUAR.value))
    else:
        sql += """
            AND peg.status_kerja = %s
        """
    ic(sql % where)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
