from datetime import date

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse

from core.enums import JENIS_MUTASI
from core.helper import get_nama_bulan
from core.services.mutasi import mutasi_data, to_excel

router = APIRouter(
    prefix="/mutasi",
    tags=["Mutasi Pegawai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{from_date}/{to_date}")
async def index(from_date: str, to_date: str, jenis_mutasi: str = Query(None, enum=[
    "PENGANGKATAN_PERTAMA", "MUTASI_LOKER", "MUTASI_JABATAN", "MUTASI_GOLONGAN", "MUTASI_GAJI", "MUTASI_GAJI_BERKALA", "TERMINASI"
])):

    result = mutasi_data(
        from_date, to_date, JENIS_MUTASI[jenis_mutasi].value if jenis_mutasi else None)
    if result.empty:
        return JSONResponse(content=None, status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/excel/{from_date}/{to_date}")
async def excel(from_date: str, to_date: str, jenis_mutasi: str = Query(None, enum=[
    "PENGANGKATAN_PERTAMA", "MUTASI_LOKER", "MUTASI_JABATAN", "MUTASI_GOLONGAN", "MUTASI_GAJI", "MUTASI_GAJI_BERKALA", "TERMINASI"
])):
    now = date.today()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    result = to_excel(
        from_date, to_date, JENIS_MUTASI[jenis_mutasi].value if jenis_mutasi else None)
    if not result:
        return JSONResponse(content=None, status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=mutasi-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
