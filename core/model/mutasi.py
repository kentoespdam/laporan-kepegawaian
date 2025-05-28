import pandas as pd

from core.config import get_connection_pool


def fetch_mutasi(from_date: str, to_date: str, jenis_mutasi: int = None) -> pd.DataFrame:
    sql = """
        SELECT
            rm.jenis_mutasi,
            peg.nipam,
            bio.nama,
            rm.tmt_berlaku,
            IFNULL(rm.nama_organisasi_lama,"") AS nama_organisasi_lama,
            IFNULL(rm.nama_jabatan_lama,"") AS nama_jabatan_lama,
            IFNULL(rm.nama_golongan,"") AS nama_golongan,
            IFNULL(rm.nama_organisasi,"") AS nama_organisasi,
            IFNULL(rm.nama_jabatan,"") AS nama_jabatan,
            IFNULL(rm.nama_golongan_lama,"") AS nama_golongan_lama,
            IFNULL(rm.notes,"") AS notes  
        FROM
            riwayat_mutasi AS rm
            INNER JOIN pegawai AS peg ON rm.pegawai_id = peg.id
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            rm.tmt_berlaku BETWEEN %s AND %s
    """
    where = (from_date, to_date)
    if jenis_mutasi is not None:
        sql += " AND rm.jenis_mutasi = %s"
        where =(from_date, to_date, jenis_mutasi)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
