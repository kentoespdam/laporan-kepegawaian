from core.config import get_connection_pool
from core.enums import STATUS_KERJA
import pandas as pd
from icecream import ic


def fetch_duk() -> pd.DataFrame:
    sql = """
        SELECT
            bio.nama,
            peg.nipam,
            gol.golongan,
            gol.pangkat,
            peg.tmt_golongan,
            jab.nama AS nama_jabatan,
            peg.tmt_jabatan,
            peg.tmt_kerja,
            TIMESTAMPDIFF(YEAR,peg.tmt_kerja,now()) AS mk_tahun,
            TIMESTAMPDIFF(MONTH,peg.tmt_kerja,now()) AS mk_bulan,
            TIMESTAMPDIFF(YEAR,bio.tanggal_lahir, now()) AS usia,
            pend.jurusan,
            pend.tahun_lulus,
            jp.nama AS tingkat_pendidikan,
            peg.status_pegawai 
        FROM
            pegawai AS peg
            INNER JOIN biodata AS bio ON peg.nik = bio.nik
            LEFT JOIN golongan AS gol ON peg.golongan_id = gol.id
            INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
            INNER JOIN pendidikan AS pend ON bio.nik = pend.biodata_id
            INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id 
        WHERE
            peg.status_kerja IN %(status_kerja)s
            AND pend.is_latest = %(is_latest)s 
        ORDER BY
            gol.golongan DESC,
            peg.tmt_golongan ASC,
            peg.status_pegawai ASC,
            peg.tmt_kerja ASC
    """
    status_kerja = [STATUS_KERJA.DIRUMAHKAN.value,
                    STATUS_KERJA.KARYAWAN_AKTIF.value]
    where = {"status_kerja": tuple(status_kerja), "is_latest": True}
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            result = cursor.fetchall()
            ic(len(result))
            # ic(sql % where)
            return pd.DataFrame(result)
