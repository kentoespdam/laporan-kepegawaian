from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse

from core.helper import get_nama_bulan
from core.model.lepas_tanggungan_anak import FILTER_LEPAS_TANGGUNGAN_ANAK
from core.services.lepas_tanggungan_anak import data_lepas_tanggungan_anak, to_excel

router = APIRouter(
    prefix="/lepas_tanggungan_anak",
    tags=["Lepas Tanggungan Anak"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def index(filter: str = Query(FILTER_LEPAS_TANGGUNGAN_ANAK.BULAN_INI.name, enum=list(filter.name for filter in FILTER_LEPAS_TANGGUNGAN_ANAK))):
    data = data_lepas_tanggungan_anak(FILTER_LEPAS_TANGGUNGAN_ANAK[filter])
    if data.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data.to_dict("records"), status_code=200)


@router.get("/export")
def excel(filter: str = Query(FILTER_LEPAS_TANGGUNGAN_ANAK.BULAN_INI.name, enum=list(filter.name for filter in FILTER_LEPAS_TANGGUNGAN_ANAK))):
    now = datetime.now()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    title_text = "Bulan: {} {}".format(bulan, tahun)

    result = to_excel(title_text, FILTER_LEPAS_TANGGUNGAN_ANAK[filter])

    if result is None:
        return JSONResponse(content={}, status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=lepas-tanggungan-anak-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
