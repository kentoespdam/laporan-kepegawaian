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