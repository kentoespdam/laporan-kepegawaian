from core.services.statistik import fetch_golongan_data
from icecream import ic

def main():
    data = fetch_golongan_data()
    ic(data.to_dict(orient="records"))
    
if __name__ == "__main__":
    main()