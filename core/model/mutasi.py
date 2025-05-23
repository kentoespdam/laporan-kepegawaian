import pandas as pd

from core.config import get_connection_pool


def fetch_mutasi(from_date: str, to_date: str, jenis_mutasi: int = None) -> pd.DataFrame:
    sql = """
        SELECT
            rw.jenis_mutasi,
            peg.nipam,
            bio.nama,
            rw.tmt_berlaku,
            IFNULL(rw.nama_organisasi_lama,"") AS nama_organisasi_lama,
            IFNULL(rw.nama_jabatan_lama,"") AS nama_jabatan_lama,
            IFNULL(rw.nama_golongan,"") AS nama_golongan,
            IFNULL(rw.nama_organisasi,"") AS nama_organisasi,
            IFNULL(rw.nama_jabatan,"") AS nama_jabatan,
            IFNULL(rw.nama_golongan_lama,"") AS nama_golongan_lama,
            IFNULL(rw.notes,"") AS notes  
        FROM
            riwayat_mutasi AS rw
            INNER JOIN pegawai AS peg ON rw.pegawai_id = peg.id
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            rw.tmt_berlaku BETWEEN %s AND %s
    """
    where = (from_date, to_date)
    if jenis_mutasi is not None:
        sql += " AND riwayat_mutasi.jenis_mutasi = %s"
        where += (jenis_mutasi,)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
