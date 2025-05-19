from core.config import get_connection_pool
import pandas as pd


def fetch_by_golongan():
    sql = """
        SELECT
            IFNULL(gol.golongan, "--") AS golongan,
            IFNULL(gol.pangkat, "--") AS pangkat,
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


def fetch_by_pendidikan_1():
    sql = """
        SELECT
            jp.nama,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik
            INNER JOIN jenjang_pendidikan AS jp ON bio.pendidikan_id = jp.id 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            jp.nama 
        ORDER BY
            jp.id DESC
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())


def fetch_by_pendidikan_2():
    pass


def fetch_by_umur():
    sql = """
        SELECT
            TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now()) AS umur,
            COUNT(TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now())) AS jumlah 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now()) 
        ORDER BY
            umur DESC
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())


def fetch_by_jenis_kelamin():
    sql = """
        SELECT
            IF(bio.jenis_kelamin = 0, "Laki-laki", "Perempuan") AS jenis_kelamin,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            bio.jenis_kelamin
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())


def fetch_by_gelar():
    sql = """
        SELECT
            jp.nama AS jenjang,
            IFNULL( pen.gelar_belakang, '--' ) AS gelar,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik
            INNER JOIN pendidikan AS pen ON bio.nik = pen.biodata_id
            INNER JOIN jenjang_pendidikan AS jp ON pen.jenjang_id = jp.id 
            AND bio.pendidikan_id = jp.id 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
            AND pen.is_latest = %s 
        GROUP BY
            pen.gelar_belakang,
            jp.id 
        ORDER BY
            jp.id DESC
    """
    where = (False, 2, True)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())


def fetch_by_agama():
    sql = """
        SELECT
            bio.agama,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            bio.agama 
        ORDER BY
            bio.agama ASC
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())


def fetch_by_status_pegawai():
    sql = """
        SELECT
            peg.status_pegawai,
            COUNT(*) AS total 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik 
        WHERE
            peg.is_deleted = %s 
            AND peg.status_kerja = %s 
        GROUP BY
            peg.status_pegawai 
        ORDER BY
            peg.status_pegawai DESC
    """
    where = (False, 2)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
