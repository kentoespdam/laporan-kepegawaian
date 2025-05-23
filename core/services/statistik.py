import pandas as pd
import swifter  # noqa: F401
from core.enums import get_status_pegawai_name
from core.helper import get_agama
from core.model.statistik import (
    fetch_by_agama,
    fetch_by_gelar,
    fetch_by_golongan,
    fetch_by_jenis_kelamin,
    fetch_by_pendidikan_1,
    fetch_by_status_pegawai,
    fetch_by_umur,
)


def fetch_golongan_data():
    data = fetch_by_golongan()
    data = data.astype({"jml_l": int, "jml_p": int, "total": int})
    data["persen"] = round(((data["total"] / data["total"].sum()) * 100), 2)
    return data


def fetch_pendidikan_1_data():
    data = fetch_by_pendidikan_1()
    data = data.astype({"total": int})
    data["persen"] = round(((data["total"] / data["total"].sum()) * 100), 2)
    return data


def fetch_pendidikan_2_data():
    pass


def fetch_umur_data():
    data = fetch_by_umur()
    data = data.astype({"total": int})
    data["persen"] = round(((data["total"] / data["total"].sum()) * 100), 2)
    range = _generate_data_umur2(data)
    range["persen"] = round(((range["total"] / range["total"].sum()) * 100), 2)
    return data, range


def _generate_data_umur2(df: pd.DataFrame) -> pd.DataFrame:
    list_range = ["<20", "20-29", "30-39", "40-49", "50-59", ">60"]
    range1 = df.query("umur < 20")["total"].sum()
    range2 = df.query("umur >= 20 and umur < 30")["total"].sum()
    range3 = df.query("umur >= 30 and umur < 40")["total"].sum()
    range4 = df.query("umur >= 40 and umur < 50")["total"].sum()
    range5 = df.query("umur >= 50 and umur < 60")["total"].sum()
    range6 = df.query("umur >= 60")["total"].sum()
    total = [range1, range2, range3, range4, range5, range6]
    return pd.DataFrame({"range": list_range, "total": total})


def fetch_jenis_kelamin_data():
    data = fetch_by_jenis_kelamin()
    data = data.astype({"total": int})
    data["persen"] = round(((data["total"] / data["total"].sum()) * 100), 2)
    return data


def fetch_gelar_data():
    data = fetch_by_gelar()
    data = data.astype({"total": int})
    data["persen"] = (data["total"] / data["total"].sum()) * 100
    return data


def fetch_agama_data():
    data = fetch_by_agama()
    data["agama"] = data["agama"].swifter.apply(lambda x: get_agama(x))
    data = data.astype({"total": int})
    data["persen"] = round(((data["total"] / data["total"].sum()) * 100), 2)
    return data


def fetch_status_pegawai_data():
    data = fetch_by_status_pegawai()
    data["status_pegawai"] = data["status_pegawai"].swifter.apply(
        lambda x: get_status_pegawai_name(x)
    )
    data = data.astype({"total": int})
    data["persen"] = (data["total"] / data["total"].sum()) * 100
    # sort data by status_pegawai
    data = data.sort_values(by="status_pegawai", ascending=False)
    return data
