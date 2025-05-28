import calendar
from datetime import datetime
from enum import Enum

import pandas as pd
from icecream import ic

from core.config import get_connection_pool


class FILTER_KENAIKAN_BERKALA(Enum):
    BULAN_INI = 0
    GTE_1 = 1
    GTE_2 = 2
    TAHUN_INI = 3


def fetch_kenaikan_berkala(filter: FILTER_KENAIKAN_BERKALA = FILTER_KENAIKAN_BERKALA.BULAN_INI) -> pd.DataFrame:
    query = """
        SELECT
            rn,
            id,
            pegawai_id,
            nipam,
            nama,
            jenis_sk,
            nomor_sk,
            tmt_berlaku,
            tmt_kenaikan,
            nama_jabatan,
            tmt_jabatan,
            golongan,
            pangkat,
            tmt_golongan,
            mkg_tahun,
            mkg_bulan,
            tmt_kerja,
            mk_tahun,
            mk_bulan,
            pendidikan_terakhir,
            tempat_lahir,
            tanggal_lahir 
        FROM
            (
            SELECT
                ROW_NUMBER() OVER ( PARTITION BY rs.pegawai_id, rs.jenis_sk ORDER BY tanggal_sk DESC ) AS rn,
                rs.id,
                rs.pegawai_id,
                peg.nipam,
                bio.nama,
                rs.jenis_sk,
                rs.nomor_sk,
                rs.tmt_berlaku,
                DATE_ADD( rs.tmt_berlaku, INTERVAL 4 YEAR ) AS tmt_kenaikan,
                jab.nama AS nama_jabatan,
                peg.tmt_jabatan,
                gol.golongan,
                gol.pangkat,
                peg.tmt_golongan,
                TIMESTAMPDIFF(YEAR, peg.tmt_golongan, CURDATE()) AS mkg_tahun,
                TIMESTAMPDIFF(MONTH, peg.tmt_golongan, CURDATE()) AS mkg_bulan,
                peg.tmt_kerja AS tmt_kerja,
                TIMESTAMPDIFF(YEAR, peg.tmt_kerja, CURDATE()) AS mk_tahun,
                TIMESTAMPDIFF(MONTH, peg.tmt_kerja, CURDATE()) AS mk_bulan,
                CONCAT_WS( " - ", jp.nama, pend.jurusan ) AS pendidikan_terakhir,
                bio.tempat_lahir,
                bio.tanggal_lahir 
            FROM
                riwayat_sk AS rs
                INNER JOIN pegawai AS peg ON rs.pegawai_id = peg.id
                INNER JOIN biodata AS bio ON peg.nik = bio.nik
                INNER JOIN golongan AS gol ON peg.golongan_id = gol.id
                INNER JOIN jabatan AS jab ON peg.jabatan_id = jab.id
                INNER JOIN pendidikan AS pend ON pend.is_latest = TRUE 
                AND bio.nik = pend.biodata_id
                INNER JOIN jenjang_pendidikan AS jp ON pend.jenjang_id = jp.id 
            WHERE
                rs.is_deleted = FALSE 
                AND rs.jenis_sk IN ( 0, 8 ) 
                AND peg.status_kerja IN ( 1, 2 ) 
                AND peg.status_pegawai = 2 
            ) AS rrn 
        WHERE
            rrn.rn = 1 
        """
    now = datetime.now()
    year = now.year
    month = now.month
    first_day = datetime(year, month, 1).strftime("%Y-%m-%d")
    last_day = datetime(year, month, calendar.monthrange(
        year, month)[1]).strftime("%Y-%m-%d")

    if filter == FILTER_KENAIKAN_BERKALA.BULAN_INI:
        query += " AND rrn.tmt_kenaikan BETWEEN %s AND %s"
        where = (first_day, last_day)
    elif filter == FILTER_KENAIKAN_BERKALA.GTE_1:
        query += " AND rrn.tmt_kenaikan BETWEEN %s AND %s"
        first_day = datetime(year, month+1, 1).strftime("%Y-%m-%d")
        last_day = datetime(year, month+1, calendar.monthrange(
            year, month+1)[1]).strftime("%Y-%m-%d")
        where = (first_day, last_day)
    elif filter == FILTER_KENAIKAN_BERKALA.GTE_2:
        query += " AND rrn.tmt_kenaikan BETWEEN %s AND %s"
        first_day = datetime(year, month+2, 1).strftime("%Y-%m-%d")
        last_day = datetime(year, month+2, calendar.monthrange(
            year, month+2)[1]).strftime("%Y-%m-%d")
        where = (first_day, last_day)
    elif filter == FILTER_KENAIKAN_BERKALA.TAHUN_INI:
        query += " AND YEAR(rrn.tmt_kenaikan) = %s"
        where = (year,)

    ic(query % where)
    with get_connection_pool() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, where)
            result = cursor.fetchall()
            return pd.DataFrame(result)
