from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from core.services.statistik import (
    fetch_agama_data,
    fetch_gelar_data,
    fetch_golongan_data,
    fetch_jenis_kelamin_data,
    fetch_pendidikan_1_data,
    fetch_status_pegawai_data,
    fetch_umur_data, fetch_pendidikan_2_data, generate_excel_pendidikan_2,
)

router = APIRouter(
    prefix="/statistik",
    tags=["Statistik Pegawai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/golongan")
async def by_golongan():
    result = fetch_golongan_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/pendidikan1")
async def by_pendidikan_1():
    result = fetch_pendidikan_1_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/pendidikan2")
async def by_pendidikan_2(tahun: int, bulan: int):
    result = fetch_pendidikan_2_data(tahun, bulan)
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/pendidikan2/excel")
async def by_pendidikan_2_excel(tahun: int, bulan: int):
    result=generate_excel_pendidikan_2(tahun, bulan)
    if result is None:
        raise HTTPException(status_code=404)
    return StreamingResponse(
        result,
        headers={
            "Content-Disposition": f"attachment; filename=pendidikan-2-{bulan}-{tahun}.xlsx"
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get("/umur")
async def by_umur():
    data, data_range = fetch_umur_data()
    if data.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(
        content={
            "umur": data.to_dict("records"),
            "range": data_range.to_dict("records"),
        },
        status_code=200,
    )


@router.get("/jenis_kelamin")
async def by_jenis_kelamin():
    result = fetch_jenis_kelamin_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/gelar_akademik")
async def by_gelar():
    result = fetch_gelar_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/agama")
async def by_agama():
    result = fetch_agama_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)


@router.get("/status_pegawai")
async def by_status_pegawai():
    result = fetch_status_pegawai_data()
    if result.empty:
        raise HTTPException(status_code=404)
    return JSONResponse(content=result.to_dict("records"), status_code=200)
