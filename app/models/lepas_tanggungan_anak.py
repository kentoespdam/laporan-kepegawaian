from datetime import datetime
from typing import Tuple

from app.core.databases import fetch_data, fetch_count_data
from app.core.enums import HubunganKeluarga, StatusKerja, StatusPendidikan, FilterLepasTanggunganAnak


class LepasTanggunganAnakModel:
    def __init__(self):
        self.filter = FilterLepasTanggunganAnak.BULAN_INI

    def fetch(self, filter_type: FilterLepasTanggunganAnak = FilterLepasTanggunganAnak.BULAN_INI):
        self.filter = filter_type
        return self._get_data()

    def count(self, filter_type: FilterLepasTanggunganAnak = FilterLepasTanggunganAnak.BULAN_INI):
        self.filter = filter_type
        return self._get_count()

    def _get_data(self):
        query = """
                SELECT pk.id,
                       pk.nama                                      AS nama_anak,
                       IF(pk.jenis_kelamin = 0, 'Pria', 'Wanita')   AS jenis_kelamin,
                       pk.tanggal_lahir,
                       TIMESTAMPDIFF(YEAR, pk.tanggal_lahir, NOW()) AS umur,
                       pk.tanggungan,
                       CASE pk.status_pendidikan
                           WHEN 0 THEN 'Belum Sekolah'
                           WHEN 1 THEN 'Sekolah'
                           ELSE 'Selesai Sekolah'
                           END                                      AS status_pendidikan,
                       bio.nama                                     AS nama_karyawan,
                       peg.nipam                                    AS nipam,
                       jab.nama                                     AS nama_jabatan
                FROM profil_keluarga pk
                         INNER JOIN biodata bio
                                    ON pk.biodata_id = bio.nik
                         INNER JOIN pegawai peg ON bio.nik = peg.nik AND peg.is_deleted = FALSE
                         INNER JOIN jabatan jab ON peg.jabatan_id = jab.id
                WHERE peg.status_kerja IN (%s, %s)
                  AND pk.hubungan_keluarga = %s
                  AND pk.status_pendidikan != %s
                  AND MONTH(pk.tanggal_lahir) = %s
                  AND TIMESTAMPDIFF(YEAR
                    , pk.tanggal_lahir
                    , STR_TO_DATE(CONCAT(%s, '-', %s, '-15'), '%%Y-%%m-%%d')
                      ) BETWEEN %s
                    AND %s \
                """

        params = self._param_builder()
        return fetch_data(query, params)

    def _get_count(self):
        query = """
                SELECT COUNT(*)
                FROM profil_keluarga pk
                         INNER JOIN biodata bio
                                    ON pk.biodata_id = bio.nik
                         INNER JOIN pegawai peg ON bio.nik = peg.nik AND peg.is_deleted = FALSE
                         INNER JOIN jabatan jab ON peg.jabatan_id = jab.id
                WHERE peg.status_kerja IN (%s, %s)
                  AND pk.hubungan_keluarga = %s
                  AND pk.status_pendidikan != %s
                  AND MONTH(pk.tanggal_lahir) = %s
                  AND TIMESTAMPDIFF(YEAR
                    , pk.tanggal_lahir
                    , STR_TO_DATE(CONCAT(%s, '-', %s, '-15'), '%%Y-%%m-%%d')
                      ) BETWEEN %s
                    AND %s \
                """

        params = self._param_builder()
        return fetch_count_data(query, params)

    def _param_builder(self):
        target_month, target_year = self._get_target_month_year()
        min_umur, max_umur = 21, 26

        return (
            StatusKerja.DIRUMAHKAN.value,
            StatusKerja.KARYAWAN_AKTIF.value,
            HubunganKeluarga.ANAK.value,
            StatusPendidikan.SELESAI_SEKOLAH.value,
            target_month,  # filter bulan lahir
            target_year, target_month,  # untuk perhitungan umur
            min_umur,
            max_umur
        )

    def _get_target_month_year(self) -> Tuple[int, int]:
        """Get target month dan year dengan handling year rollover yang lebih robust."""
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        adjustment = self.filter.value

        # Calculate target month and year
        total_months = current_month + adjustment
        target_year = current_year + (total_months - 1) // 12
        target_month = (total_months - 1) % 12 + 1

        return target_month, target_year
