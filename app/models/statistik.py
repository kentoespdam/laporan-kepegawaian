from app.core.databases import fetch_data
from app.core.enums import StatusKerja


def fetch_by_golongan():
    sql = """
          SELECT IFNULL(gol.golongan, '--')           AS golongan,
                 IFNULL(gol.pangkat, '--')            AS pangkat,
                 SUM(IF(bio.jenis_kelamin = 0, 1, 0)) AS jml_l,
                 SUM(IF(bio.jenis_kelamin = 1, 1, 0)) AS jml_p,
                 COUNT(*)                             AS total
          FROM pegawai AS peg
                   LEFT JOIN golongan AS gol ON peg.golongan_id = gol.id
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY gol.id \
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)


def fetch_by_pendidikan_1():
    sql = """
          SELECT jp.nama,
                 COUNT(*) AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
                   INNER JOIN jenjang_pendidikan AS jp ON bio.pendidikan_id = jp.id
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY jp.id, jp.nama
          ORDER BY jp.id DESC
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)


def fetch_by_pendidikan_2(tahun: int, bulan=int):
    sql = """
          SELECT speg.id,
                 speg.pendidikan,
                 speg.non_golongan,
                 speg.golongan_a,
                 speg.golongan_b,
                 speg.golongan_c,
                 speg.golongan_d,
                 speg.non_golongan + speg.golongan_a + speg.golongan_b + speg.golongan_c +
                 speg.golongan_d                                       AS jml_golongan,
                 speg.kontrak,
                 speg.capeg,
                 speg.honorer,
                 speg.tetap,
                 speg.kontrak + speg.capeg + speg.honorer + speg.tetap AS jml_status_pegawai,
                 speg.adm,
                 speg.pelayanan,
                 speg.teknik,
                 speg.adm + speg.pelayanan + speg.teknik               AS jml_unit_kerja,
                 speg.pria,
                 speg.wanita,
                 speg.pria + speg.wanita                               AS jml_jenis_kelamin
          FROM statistik_pegawai AS speg
          WHERE speg.tahun = %s
            AND speg.bulan = %s
          ORDER BY speg.seq
          """
    where = (tahun, bulan)
    return fetch_data(sql, where)


def fetch_by_umur():
    sql = """
          SELECT TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now())        AS umur,
                 COUNT(TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now())) AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now())
          ORDER BY umur DESC \
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)


def fetch_by_jenis_kelamin():
    sql = """
          SELECT IF(bio.jenis_kelamin = 0, 'Laki-laki', 'Perempuan') AS jenis_kelamin,
                 COUNT(*)                                            AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY bio.jenis_kelamin \
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)


def fetch_by_gelar():
    sql = """
          SELECT jp.nama                          AS jenjang,
                 IFNULL(pen.gelar_belakang, '--') AS gelar,
                 COUNT(*)                         AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
                   INNER JOIN pendidikan AS pen ON bio.nik = pen.biodata_id
                   INNER JOIN jenjang_pendidikan AS jp ON pen.jenjang_id = jp.id
              AND bio.pendidikan_id = jp.id
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
            AND pen.is_latest = %s
          GROUP BY pen.gelar_belakang,
                   jp.id
          ORDER BY jp.id DESC \
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value, True)

    return fetch_data(sql, where)


def fetch_by_agama():
    sql = """
          SELECT bio.agama,
                 COUNT(*) AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY bio.agama
          ORDER BY bio.agama
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)


def fetch_by_status_pegawai():
    sql = """
          SELECT peg.status_pegawai,
                 COUNT(*) AS total
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
          WHERE peg.is_deleted = %s
            AND peg.status_kerja = %s
          GROUP BY peg.status_pegawai
          ORDER BY peg.status_pegawai DESC \
          """
    where = (False, StatusKerja.KARYAWAN_AKTIF.value)

    return fetch_data(sql, where)
