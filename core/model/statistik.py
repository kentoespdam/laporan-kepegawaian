from config import get_connection_pool
import pandas as pd

def fetch_by_golongan():
    sql = """
        SELECT
            gol.id,
            gol.golongan,
            gol.pangkat,
            SUM( CASE WHEN bio.jenis_kelamin = 0 THEN 1 ELSE 0 END ) AS jml_l,
            SUM( CASE WHEN bio.jenis_kelamin = 1 THEN 1 ELSE 0 END ) AS jml_p,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            LEFT JOIN golongan AS gol ON peg.golongan_id = gol.id
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            gol.id
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
