from core.model.duk import fetch_duk
from icecream import ic
import pandas as pd
import swifter


def main():
    data = fetch_duk()
    data = cleanup(data)
    ic(data.to_dict(orient='records'))
    ic(data["nipam"].size)


def cleanup(df: pd.DataFrame) -> pd.DataFrame:
    df["tmt_golongan"] = df["tmt_golongan"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["tmt_jabatan"] = df["tmt_jabatan"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["tmt_kerja"] = df["tmt_kerja"].swifter.apply(
        lambda x: x.strftime("%d.%m.%Y") if x is not None else None)
    df["mk_bulan"] = df.swifter.apply(lambda x: hitung_sisa_bulan(x), axis=1)
    return df


def hitung_sisa_bulan(row: pd.Series):
    tahun = row["mk_tahun"]
    bulan = row["mk_bulan"]
    sisa = bulan-tahun*12
    return sisa


if __name__ == "__main__":
    main()
