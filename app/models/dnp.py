import pandas as pd

from app.core.config import fetch_data
from app.core.enums import StatusKerja


def fetch_dnp() -> pd.DataFrame:
    sql = """
          SELECT org.kode                                                AS kode_organisasi,
                 jabatan.level_id                                        AS level_jabatan,
                 bio.nama,
                 peg.nipam,
                 jabatan.nama                                            AS nama_jabatan,
                 DATE_FORMAT(peg.tmt_jabatan, '%%d.%%m.%%Y')             AS tmt_jabatan,
                 gol.pangkat,
                 gol.golongan,
                 DATE_FORMAT(peg.tmt_golongan, '%%d.%%m.%%Y')            AS tmt_golongan,
                 TIMESTAMPDIFF(
                         YEAR,
                         peg.tmt_golongan,
                         now())                                          AS mkg_tahun,
                 TIMESTAMPDIFF(
                         MONTH,
                         peg.tmt_golongan,
                         now())                                          AS mkg_bulan,
                 DATE_FORMAT(peg.tmt_kerja, '%%d.%%m.%%Y')               AS tmt_kerja,
                 TIMESTAMPDIFF(
                         YEAR,
                         peg.tmt_kerja,
                         now())                                          AS mk_tahun,
                 TIMESTAMPDIFF(
                         MONTH,
                         peg.tmt_kerja,
                         now())                                          AS mk_bulan,
                 CONCAT_WS(' ', jp.nama, pend.jurusan, pend.tahun_lulus) AS pendidikan,
                 CONCAT_WS(
                         ' ',
                         bio.tempat_lahir,
                         DATE_FORMAT(bio.tanggal_lahir, '%%d.%%m.%%Y'))  AS ttl
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
                   INNER JOIN jabatan ON peg.jabatan_id = jabatan.id
                   LEFT JOIN golongan AS gol ON peg.golongan_id = gol.id
                   LEFT JOIN organisasi AS org ON peg.organisasi_id = org.id
                   LEFT JOIN pendidikan AS pend ON bio.nik = pend.biodata_id
                   INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id
              AND bio.pendidikan_id = jp.id
          WHERE peg.status_kerja IN %s
            AND pend.is_latest = %s
          ORDER BY org.kode, jabatan.level_id, peg.tmt_kerja
          """

    status_kerja = (StatusKerja.DIRUMAHKAN.value, StatusKerja.KARYAWAN_AKTIF.value,)
    params = (status_kerja, True)
    return fetch_data(sql, params)
