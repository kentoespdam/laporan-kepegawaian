import pandas as pd

from app.core.databases import fetch_data


def fetch_mutasi(from_date: str, to_date: str, jenis_mutasi: int = None) -> pd.DataFrame:
    sql = """
          SELECT rm.jenis_mutasi,
                 rm.nipam,
                 rm.nama,
                 rm.tmt_berlaku,
                 IFNULL(rm.nama_organisasi_lama, '') AS nama_organisasi_lama,
                 IFNULL(rm.nama_jabatan_lama, '')    AS nama_jabatan_lama,
                 IFNULL(rm.nama_golongan, '')        AS nama_golongan,
                 IFNULL(rm.nama_organisasi, '')      AS nama_organisasi,
                 IFNULL(rm.nama_jabatan, '')         AS nama_jabatan,
                 IFNULL(rm.nama_golongan_lama, '')   AS nama_golongan_lama,
                 IFNULL(rm.notes, '')                AS notes
          FROM riwayat_mutasi AS rm
          WHERE rm.tmt_berlaku BETWEEN %s AND %s \
          """
    where = (from_date, to_date,)
    if jenis_mutasi is not None:
        sql += " AND rm.jenis_mutasi = %s"
        where += (jenis_mutasi,)

    return fetch_data(sql, where)
