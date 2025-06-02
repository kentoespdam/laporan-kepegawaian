from datetime import date, datetime
from enum import Enum

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse

from core.helper import get_nama_bulan
from core.model.kenaikan_berkala import FILTER_KENAIKAN_BERKALA
from core.services.kenaikan_berkala import kenaikan_berkala_data, to_excel

router = APIRouter(
    prefix="/kenaikan_berkala",
    tags=["Kenaikan Pangkat/Gaji Berkala"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def index(filter: str = Query(FILTER_KENAIKAN_BERKALA.BULAN_INI.name, enum=list(filter.name for filter in FILTER_KENAIKAN_BERKALA))):
    data = kenaikan_berkala_data(FILTER_KENAIKAN_BERKALA[filter])
    if data.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data.to_dict("records"), status_code=200)

@router.get("/excel")
def excel(filter: str = Query(FILTER_KENAIKAN_BERKALA.BULAN_INI.name, enum=list(filter.name for filter in FILTER_KENAIKAN_BERKALA))):
    now = datetime.now()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    title_text = "Bulan: {} {}".format(bulan, tahun)

    result = to_excel(title_text, FILTER_KENAIKAN_BERKALA[filter])

    if result is None:
        return JSONResponse(content={}, status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=kenaikan-berkala-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )