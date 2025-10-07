from app.core.config import fetch_data

from app.core.enums import StatusKerja


def fetch_struktur_organisasi():
    sql = """
          SELECT jab.id                   AS `key`,
                 IFNULL(jab.parent_id, 0) AS boss,
                 jab.level_id             AS `level`,
                 jab.nama                 AS jabatan,
                 IFNULL(bio.nama, '')     AS name,
                 IFNULL(peg.nipam, '')    AS nik
          FROM jabatan AS jab
                   LEFT JOIN pegawai AS peg ON jab.id = peg.jabatan_id AND status_kerja = %s
                   LEFT JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE jab.is_deleted = %s
            AND jab.level_id <= %s \
          """
    where = (StatusKerja.KARYAWAN_AKTIF.value, False, 6)

    return fetch_data(sql, where)
