from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from app.core.enums import FilterLepasTanggunganAnak
from app.core.helper import get_nama_bulan
from app.services.lepas_tanggungan_anak import LepasTanggunganAnakService

router = APIRouter(
    prefix="/lepas_tanggungan_anak",
    tags=["Lepas Tanggungan Anak"],
    responses={404: {"description": "Not found"}},
)

service = LepasTanggunganAnakService()


@router.get("/")
def index(filter: str = Query(FilterLepasTanggunganAnak.BULAN_INI.name,
                              enum=list(filter.name for filter in FilterLepasTanggunganAnak))):
    data = service.fetch(FilterLepasTanggunganAnak[filter])
    if data.empty:
        raise HTTPException(status_code=404, detail="Not found")
    return JSONResponse(content=data.to_dict("records"), status_code=200)


@router.get("/count")
def count(filter: str = Query(FilterLepasTanggunganAnak.BULAN_INI.name,
                              enum=list(filter.name for filter in FilterLepasTanggunganAnak))):
    data = service.fetch_count(FilterLepasTanggunganAnak[filter])
    return JSONResponse(content={"count": data}, status_code=200)


@router.get("/excel")
def excel(filter: str = Query(FilterLepasTanggunganAnak.BULAN_INI.name,
                              enum=list(filter.name for filter in FilterLepasTanggunganAnak))):
    now = datetime.now()
    tahun = now.year
    bulan = get_nama_bulan(now.month)
    title_text = "Bulan: {} {}".format(bulan, tahun)

    result = service.to_excel(title_text, FilterLepasTanggunganAnak[filter])

    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=lepas-tanggungan-anak-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
