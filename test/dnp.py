from core.model.organisasi import fetch_kode_nama_organisasi
from core.services.dnp import dnp_data
from icecream import ic


def main():
    data = dnp_data()
    ic(data["dnp"].query("nama_jabatan.str.startswith('Direktur')").to_dict(orient='records'))

if __name__ == "__main__":
    main()
