from datetime import date
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from core.services.dnp import fetch_dnp_data, to_excel
from core.helper import get_nama_bulan
router = APIRouter(
    prefix="/dnp",
    tags=["Daftar Nominatif Pegawai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index():
    result = fetch_dnp_data()
    if result["dnp"].empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={
        "data": result["dnp"].to_dict("records"),
        "organisasi": result["organisasi"].to_dict("records")
    }, status_code=200)


@router.get("/excel")
async def excel():
    now = date.today()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    result = to_excel(tahun, bulan)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=nominatif-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
