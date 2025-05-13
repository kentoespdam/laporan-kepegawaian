from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from core.model.so import fetch_struktur_organisasi
from core.services.so import fetch_hierarchy
from icecream import ic

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


@router.get("/hierarchy")
async def hierarchy():
    data_so = fetch_hierarchy()
    ic(data_so)
    if data_so is None:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data_so, status_code=200)


@router.get("/gojs")
async def gojs():
    data_so = fetch_struktur_organisasi()
    if data_so is None:
        return JSONResponse(content={}, status_code=404)
    return JSONResponse(content=data_so, status_code=200)


@router.get("/template", response_class=HTMLResponse)
async def template(request: Request):
    data_so = fetch_struktur_organisasi()
    return templates.TemplateResponse(
        request=request,
        name="so.html",
        context={"data_so": data_so.to_dict("records")},
    )
