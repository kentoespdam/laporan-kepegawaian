import pandas as pd

from core.config import get_connection_pool


def fetch_mutasi(from_date: str, to_date: str, jenis_mutasi: int = None) -> pd.DataFrame:
    sql = """
        SELECT
            riwayat_mutasi.jenis_mutasi,
            pegawai.nipam,
            biodata.nama,
            riwayat_mutasi.tmt_berlaku,
            riwayat_mutasi.nama_jabatan_lama,
            riwayat_mutasi.nama_jabatan 
        FROM
            riwayat_mutasi
            INNER JOIN pegawai ON riwayat_mutasi.pegawai_id = pegawai.id
            INNER JOIN biodata ON pegawai.nik = biodata.nik 
        WHERE
            riwayat_mutasi.tmt_berlaku BETWEEN %s AND %s
    """
    where = (from_date, to_date)
    if jenis_mutasi is not None:
        sql += " AND riwayat_mutasi.jenis_mutasi = %s"
        where += (jenis_mutasi,)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
