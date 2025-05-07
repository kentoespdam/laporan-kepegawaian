from core.config import get_connection_pool
import pandas as pd
from icecream import ic


def fetch_kode_nama_organisasi(level_org: int = None) -> pd.DataFrame:
    sql = """
        SELECT
            kode,
            nama
        FROM
            organisasi
        WHERE
            is_deleted = %(is_deleted)s
    """
    where = {"is_deleted": False}
    if level_org is not None:
        sql += " AND level_org = %(level_id)s"
        where = {"is_deleted": False, "level_id": level_org}
        
    # sql +=" ORDER BY parent_id, kode ASC "

    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, where)
            return pd.DataFrame(cursor.fetchall())
