import pandas as pd

from core.config import fetch_data


def fetch_kode_nama_organisasi(level_org: int = None) -> pd.DataFrame:
    sql = """
          SELECT kode,
                 nama
          FROM organisasi
          WHERE is_deleted = %(is_deleted)s \
          """
    where = {"is_deleted": False}
    if level_org is not None:
        sql += " AND level_org = %(level_id)s"
        where = {"is_deleted": False, "level_id": level_org}

    return fetch_data(sql, where)
