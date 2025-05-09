from core.config import get_connection_pool
import pandas as pd

from core.enums import STATUS_KERJA


def fetch_struktur_organisasi():
    sql = """
        SELECT
            jab.id AS `key`,
            IFNULL(jab.parent_id,0) AS boss,
            jab.level_id AS `level`,
            jab.nama AS jabatan,
            IFNULL(bio.nama, "") AS name,
            IFNULL(peg.nipam, "") AS nik
        FROM
            jabatan AS jab
            LEFT JOIN pegawai AS peg ON jab.id = peg.jabatan_id AND status_kerja=%s
            LEFT JOIN biodata AS bio ON peg.nik = bio.nik
        WHERE
            jab.is_deleted = %s 
            AND jab.level_id <= %s
    """
    where = (STATUS_KERJA.KARYAWAN_AKTIF.value, False, 6)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
