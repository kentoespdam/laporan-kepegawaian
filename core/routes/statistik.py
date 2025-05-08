from fastapi import APIRouter
from fastapi.responses import JSONResponse
from core.services.statistik import (
    fetch_agama_data,
    fetch_gelar_data,
    fetch_golongan_data,
    fetch_jenis_kelamin_data,
    fetch_pendidikan_1_data,
    fetch_status_pegawai_data,
    fetch_umur_data,
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
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)


@router.get("/pendidikan1")
async def by_pendidikan_1():
    result = fetch_pendidikan_1_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)


@router.get("/pendidikan2")
async def by_pendidikan_2():
    return JSONResponse(content={}, status_code=200)


@router.get("/umur")
async def by_umur():
    data, range = fetch_umur_data()
    if data.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(
        content={
            "content": {
                "umur": data.to_dict("records"),
                "range": range.to_dict("records"),
            }
        },
        status_code=200,
    )


@router.get("/jenis_kelamin")
async def by_jenis_kelamin():
    result = fetch_jenis_kelamin_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)


@router.get("/gelar_akademik")
async def by_gelar():
    result = fetch_gelar_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)


@router.get("/agama")
async def by_agama():
    result = fetch_agama_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)


@router.get("/status_pegawai")
async def by_status_pegawai():
    result = fetch_status_pegawai_data()
    if result.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content={"content": result.to_dict("records")}, status_code=200)
