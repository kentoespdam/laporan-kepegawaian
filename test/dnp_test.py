from core.services.dnp import fetch_dnp_data
from icecream import ic


def main():
    data = fetch_dnp_data()
    ic(data["dnp"].query("nama_jabatan.str.startswith('Direktur')").to_dict(orient='records'))

if __name__ == "__main__":
    main()
