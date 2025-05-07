from datetime import date
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from core.services.duk import duk_data, to_excel
from core.helper import get_nama_bulan
router = APIRouter(
    prefix="/duk",
    tags=["Daftar Urut Kepangkatan"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index():
    result = duk_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/excel")
async def excel():
    now = date.today()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    result = to_excel(tahun, bulan)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=duk-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
