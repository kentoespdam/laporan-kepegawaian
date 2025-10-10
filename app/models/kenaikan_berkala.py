from datetime import datetime

import pandas as pd

from app.core.databases import fetch_data, fetch_count_data
from app.core.enums import FilterKenaikanBerkala, JenisSk, StatusKerja, StatusPegawai


class KenaikanBerkalaModel:
    def __init__(self):
        self.data = pd.DataFrame()

    def fetch(self, filter: FilterKenaikanBerkala = FilterKenaikanBerkala.BULAN_INI,
              jenis_sk: JenisSk = JenisSk.SK_KENAIKAN_GAJI_BERKALA):
        query = self._query_builder(self._base_query(), filter)
        where = self._condition_builder(self._base_condition(jenis_sk), filter)

        df = fetch_data(query, where)
        return df

    def fetch_count(self, filter: FilterKenaikanBerkala = FilterKenaikanBerkala.BULAN_INI,
                    jenis_sk: JenisSk = JenisSk.SK_KENAIKAN_GAJI_BERKALA):
        query = self._query_builder(self._base_count_query(), filter)
        where = self._condition_builder(self._base_condition(jenis_sk), filter)
        count = fetch_count_data(query, where)
        return count

    @staticmethod
    def _base_condition(jenis_sk: JenisSk):
        return (
            False,  # pegawai.is_deleted
            (StatusKerja.DIRUMAHKAN.value, StatusKerja.KARYAWAN_AKTIF.value,),  # pegawai.status_kerja
            StatusPegawai.PEGAWAI.value,  # pegawai.status_pegawai
            True,  # pendidikan is_latest
            False,  # riwayat_sk.is_deleted
            jenis_sk.value  # jenis sk
        )

    @staticmethod
    def _condition_builder(base_condition: tuple, filter: FilterKenaikanBerkala = FilterKenaikanBerkala.BULAN_INI):
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        # Handle month adjustments using mapping
        month_adjustments = {
            FilterKenaikanBerkala.GTE_1: 1,
            FilterKenaikanBerkala.GTE_2: 2
        }

        if filter in month_adjustments:
            adjustment = month_adjustments[filter]
            current_month += adjustment
            if current_month > 12:
                current_month -= 12
                current_year += 1

        # Build final condition
        if filter == FilterKenaikanBerkala.TAHUN_INI:
            base_condition += (current_year, current_year)
        else:
            base_condition += (current_year, current_month, current_year, current_month)

        return base_condition

    @staticmethod
    def _query_builder(query: str, filter: FilterKenaikanBerkala):
        if filter == FilterKenaikanBerkala.TAHUN_INI:
            query += """
                AND (YEAR(rs.kenaikan_berikutnya)=%s OR YEAR(rsp.tanggal_eksekusi_sanksi)=%s) 
            """
        else:
            query += """
                AND YEAR(rs.kenaikan_berikutnya) = %s
                AND MONTH(rs.kenaikan_berikutnya) = %s
                OR(
                    YEAR(rsp.tanggal_eksekusi_sanksi) = %s
                    AND MONTH(rsp.tanggal_eksekusi_sanksi) = %s
                )
            """
        return query

    @staticmethod
    def _base_query():
        return """
               SELECT rs.id,
                      rs.pegawai_id,
                      peg.nipam,
                      bio.nama,
                      rs.jenis_sk,
                      rs.nomor_sk,
                      rs.tmt_berlaku,
                      rs.kenaikan_berikutnya,
                      rsp.tanggal_eksekusi_sanksi,
                      ssp.is_pending_gaji,
                      ssp.is_pending_pangkat,
                      jab.nama                              AS nama_jabatan,
                      peg.tmt_jabatan,
                      gol.golongan,
                      gol.pangkat,
                      peg.tmt_golongan,
                      TIMESTAMPDIFF(
                              YEAR,
                              peg.tmt_golongan,
                              CURDATE())                    AS mkg_tahun,
                      TIMESTAMPDIFF(
                              MONTH,
                              peg.tmt_golongan,
                              CURDATE())                    AS mkg_bulan,
                      peg.tmt_kerja,
                      TIMESTAMPDIFF(
                              YEAR,
                              peg.tmt_kerja,
                              CURDATE())                    AS mk_tahun,
                      TIMESTAMPDIFF(
                              MONTH,
                              peg.tmt_kerja,
                              CURDATE())                    AS mk_bulan,
                      CONCAT_WS('-', jp.nama, pend.jurusan) AS pendidikan_terakhir,
                      bio.tempat_lahir,
                      bio.tanggal_lahir
               FROM riwayat_sk AS rs
                        INNER JOIN pegawai AS peg ON rs.pegawai_id = peg.id
                   AND peg.is_deleted = %s
                   AND peg.status_kerja IN %s
                   AND peg.status_pegawai = %s
                        INNER JOIN biodata AS bio ON peg.nik = bio.nik
                        INNER JOIN golongan AS gol ON peg.golongan_id = gol.id
                        INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
                        INNER JOIN pendidikan AS pend ON bio.nik = pend.biodata_id AND pend.is_latest = %s
                        INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id
                        LEFT JOIN riwayat_sp AS rsp ON peg.id = rsp.pegawai_id
                        LEFT JOIN sanksi_sp AS ssp ON rsp.sanksi_id = ssp.id
               WHERE rs.is_deleted = %s
                 AND rs.jenis_sk = %s \
               """

    @staticmethod
    def _base_count_query():
        return """
               SELECT COUNT(*)
               FROM riwayat_sk AS rs
                        INNER JOIN pegawai AS peg ON rs.pegawai_id = peg.id
                   AND peg.is_deleted = %s
                   AND peg.status_kerja IN %s
                   AND peg.status_pegawai = %s
                        INNER JOIN biodata AS bio ON peg.nik = bio.nik
                        INNER JOIN golongan AS gol ON peg.golongan_id = gol.id
                        INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
                        INNER JOIN pendidikan AS pend ON bio.nik = pend.biodata_id AND pend.is_latest = %s
                        INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id
                        LEFT JOIN riwayat_sp AS rsp ON peg.id = rsp.pegawai_id
                        LEFT JOIN sanksi_sp AS ssp ON rsp.sanksi_id = ssp.id
               WHERE rs.is_deleted = %s
                 AND rs.jenis_sk = %s \
               """
