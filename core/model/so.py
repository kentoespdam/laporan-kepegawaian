from core.config import get_connection_pool
import pandas as pd


def fetch_struktur_organisasi():
    sql = """
        SELECT
            jab.id AS `key`,
            jab.parent_id AS boss,
            jab.nama AS jabatan,
            jab.level_id AS level,
            bio.nama AS `name`,
            peg.nipam AS nik 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik
            INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
            AND jab.level_id < %s
    """
    where = (False, 2, 7)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
