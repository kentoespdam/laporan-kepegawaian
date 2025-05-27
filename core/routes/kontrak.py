from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse
from core.helper import get_nama_bulan
from core.model.kontrak import FILTER_KONTRAK
# from icecream import ic

from core.services.kontrak import kontrak_data, to_excel

router = APIRouter(
    prefix="/kontrak",
    tags=["Monitoring Kontrak"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index(filter: str = Query("AKTIF", enum=list(filter_kontrak.name for filter_kontrak in FILTER_KONTRAK))):
    data = kontrak_data(FILTER_KONTRAK[filter])
    if data.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data.to_dict("records"), status_code=200)


@router.get("/excel")
async def excel(filter: str = Query("AKTIF", enum=list(filter_kontrak.name for filter_kontrak in FILTER_KONTRAK))):
    now = datetime.now()
    tahun = now.year
    if filter == "GTE_1_MONTH":
        bulan = get_nama_bulan(now.month+1)
        title_text= "Berakhir Bulan {} {}".format(bulan, tahun)
    elif filter == "GTE_2_MONTH":
        bulan = get_nama_bulan(now.month+2)
        title_text= "Berakhir Bulan {} {}".format(bulan, tahun)
    elif filter == "GTE_3_MONTH":
        bulan = get_nama_bulan(now.month+3)
        title_text= "Berakhir Bulan {} {}".format(bulan, tahun)
    elif filter == "ENDED":
        bulan = get_nama_bulan(now.month+4)
        title_text= "Telah Berakhir Bulan {} {}".format(bulan, tahun)
    else:
        bulan = get_nama_bulan(now.month)
        title_text= "Bulan {} {}".format(bulan, tahun)

    result = to_excel(title_text, FILTER_KONTRAK[filter])
    if result is None:
        return JSONResponse(content={}, status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=monitoring-kontrak-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
