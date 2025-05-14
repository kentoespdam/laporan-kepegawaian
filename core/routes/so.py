from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from core.model.so import fetch_struktur_organisasi

router = APIRouter(
    prefix="/so",
    tags=["Struktur Organisasi"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="core/views")


@router.get("/")
async def index():
    data_so = fetch_struktur_organisasi()
    if data_so.empty:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data_so.to_dict("records"), status_code=200)