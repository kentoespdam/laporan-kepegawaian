from enum import Enum


class StatusPegawai(Enum):
    KONTRAK = 0
    CAPEG = 1
    PEGAWAI = 2
    CALON_HONORER = 3
    HONORER = 4
    NON_PEGAWAI = 5

class StatusKerja(Enum):
    BERHENTI_OR_KELUAR = 0
    DIRUMAHKAN = 1
    KARYAWAN_AKTIF = 2
    LAMARAN_BARU = 3
    TAHAP_SELEKSI = 4
    DITERIMA = 5
    DIREKOMENDASIKAN = 6
    DITOLAK = 7


class JenisMutasi(Enum):
    PENGANGKATAN_PERTAMA = 0
    MUTASI_LOKER = 1
    MUTASI_JABATAN = 2
    MUTASI_GOLONGAN = 3
    MUTASI_GAJI = 4
    MUTASI_GAJI_BERKALA = 5
    TERMINASI = 6


class JenisSk(Enum):
    SK_KENAIKAN_PANGKAT_GOLONGAN = 0
    SK_CAPEG = 1
    SK_PEGAWAI_TETAP = 2
    SK_JABATAN = 3
    SK_MUTASI = 4
    SK_PENSIUN = 5
    SK_LAINNYA = 6
    SK_PENYESUAIAN_GAJI = 7
    SK_KENAIKAN_GAJI_BERKALA = 8

class FilterKenaikanBerkala(Enum):
    BULAN_INI = 0
    GTE_1 = 1
    GTE_2 = 2
    TAHUN_INI = 3

class HubunganKeluarga(Enum):
    SUAMI = 0
    ISTRI = 1
    AYAH = 2
    IBU = 3
    ANAK = 4
    SAUDARA = 5

class StatusPendidikan(Enum):
    BELUM_SEKOLAH = 0
    SEKOLAH = 1
    SELESAI_SEKOLAH = 2