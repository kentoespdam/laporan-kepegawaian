from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from core.helper import get_nama_bulan
from core.model.kenaikan_berkala import FilterKenaikanBerkala
from core.services.kenaikan_berkala import kenaikan_berkala_data, to_excel

router = APIRouter(
    prefix="/kenaikan_berkala",
    tags=["Kenaikan Pangkat/Gaji Berkala"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def index(filter: str = Query(FilterKenaikanBerkala.BULAN_INI.name, enum=list(filter.name for filter in FilterKenaikanBerkala))):
    data = kenaikan_berkala_data(FilterKenaikanBerkala[filter])
    if data.empty:
        raise HTTPException(status_code=404, detail="Data Not found")
    return JSONResponse(content=data.to_dict("records"), status_code=200)

@router.get("/excel")
def excel(filter: str = Query(FilterKenaikanBerkala.BULAN_INI.name, enum=list(filter.name for filter in FilterKenaikanBerkala))):
    now = datetime.now()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    title_text = "Bulan: {} {}".format(bulan, tahun)

    result = to_excel(title_text, FilterKenaikanBerkala[filter])

    if result is None:
        return JSONResponse(content={}, status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=kenaikan-berkala-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )