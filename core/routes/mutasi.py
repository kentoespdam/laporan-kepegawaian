from datetime import date

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from core.enums import JenisMutasi
from core.helper import get_nama_bulan
from core.services.mutasi import mutasi_data, to_excel

router = APIRouter(
    prefix="/mutasi",
    tags=["Mutasi Pegawai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{from_date}/{to_date}")
async def index(from_date: str, to_date: str,
                jenis_mutasi: str = Query(None, enum=list(jenis.name for jenis in JenisMutasi))):
    result = mutasi_data(
        from_date, to_date, JenisMutasi[jenis_mutasi].value if jenis_mutasi is not None else None)
    if result.empty:
        raise HTTPException(status_code=404, detail="Not found")
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/excel/{from_date}/{to_date}")
async def excel(from_date: str, to_date: str,
                jenis_mutasi: str = Query(None, enum=list(jenis.name for jenis in JenisMutasi))):
    now = date.today()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    result = to_excel(
        from_date, to_date, JenisMutasi[jenis_mutasi].value if jenis_mutasi is not None else None)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=mutasi-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
