from datetime import date
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from core.services.duk import duk_data, to_excel
from core.helper import get_nama_bulan
from icecream import ic

router = APIRouter(
    prefix="/statistik",
    tags=["Statistik Pegawai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/golongan")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/pendidikan1")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/pendidikan2")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/umur")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/jenis_kelamin")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/gelar_akademik")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/agama")
async def index():
    return JSONResponse(content={}, status_code=200)

@router.get("/status_pegawai")
async def index():
    return JSONResponse(content={}, status_code=200)
