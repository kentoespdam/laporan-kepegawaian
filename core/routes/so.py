from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.model.so import fetch_struktur_organisasi

router = APIRouter(
    prefix="/so",
    tags=["Struktur Organisasi"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="core/views")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data_so = fetch_struktur_organisasi()
    return templates.TemplateResponse(
        request=request,
        name="so.html",
        context={"data_so": data_so.to_dict("records")},
    )
