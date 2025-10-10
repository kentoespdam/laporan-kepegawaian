import pandas as pd

from app.core.databases import fetch_data
from app.core.enums import StatusKerja


def fetch_duk() -> pd.DataFrame:
    sql = """
          SELECT bio.nama,
                 peg.nipam,
                 gol.golongan,
                 gol.pangkat,
                 peg.tmt_golongan,
                 jab.nama                                      AS nama_jabatan,
                 peg.tmt_jabatan,
                 peg.tmt_kerja,
                 TIMESTAMPDIFF(YEAR, peg.tmt_kerja, now())     AS mk_tahun,
                 TIMESTAMPDIFF(MONTH, peg.tmt_kerja, now())    AS mk_bulan,
                 TIMESTAMPDIFF(YEAR, bio.tanggal_lahir, now()) AS usia,
                 pend.jurusan,
                 pend.tahun_lulus,
                 jp.nama                                       AS tingkat_pendidikan,
                 peg.status_pegawai
          FROM pegawai AS peg
                   INNER JOIN biodata AS bio ON peg.nik = bio.nik
                   LEFT JOIN golongan AS gol ON peg.golongan_id = gol.id
                   INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
                   INNER JOIN pendidikan AS pend ON bio.nik = pend.biodata_id
                   INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id
          WHERE peg.status_kerja IN %(status_kerja)s
            AND pend.is_latest = %(is_latest)s
          ORDER BY gol.golongan DESC, peg.tmt_golongan, peg.status_pegawai, peg.tmt_kerja \
          """
    status_kerja = [StatusKerja.DIRUMAHKAN.value,
                    StatusKerja.KARYAWAN_AKTIF.value]
    where = {"status_kerja": tuple(status_kerja), "is_latest": True}
    return fetch_data(sql, where)
