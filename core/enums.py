from enum import Enum


class STATUS_PEGAWAI(Enum):
    KONTRAK = 0
    CAPEG = 1
    PEGAWAI = 2
    CALON_HONORER = 3
    HONORER = 4
    NON_PEGAWAI = 5

def get_status_pegawai_name(id):
    switcher = {
        0: "Pegawai Kontak",
        1: "Calon Pegawai",
        2: "Pegawai Tetap",
        3: "Calon Honorer Tetap",
        4: "Honorer Tetap",
        5: "Non Pegawai"
    }
    return switcher.get(id, "Invalid ID")

class STATUS_KERJA(Enum):
    BERHENTI_OR_KELUAR = 0
    DIRUMAHKAN = 1
    KARYAWAN_AKTIF = 2
    LAMARAN_BARU = 3
    TAHAP_SELEKSI = 4
    DITERIMA = 5
    DIREKOMENDASIKAN = 6
    DITOLAK = 7

class JENIS_MUTASI(Enum):
    PENGANGKATAN_PERTAMA=0
    MUTASI_LOKER=1
    MUTASI_JABATAN=2
    MUTASI_GOLONGAN=3
    MUTASI_GAJI=4
    MUTASI_GAJI_BERKALA=5
    TERMINASI=6

def get_jenis_mutasi_name(id):
    switcher = {
        0: "Pengangkatan Pertama",
        1: "Mutasi Lokasi Kerja",
        2: "Mutasi Jabatan",
        3: "Mutasi Golongan",
        4: "Mutasi Gaji",
        5: "Mutasi Gaji Berkala",
        6: "Terminasi"
    }
    return switcher.get(id, "Invalid ID")