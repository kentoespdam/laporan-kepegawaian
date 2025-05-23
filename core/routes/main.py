from fastapi import APIRouter


from . import dnp, duk, so, statistik, mutasi
api_router = APIRouter()

api_router.include_router(duk.router)
api_router.include_router(dnp.router)
api_router.include_router(so.router)
api_router.include_router(statistik.router)
api_router.include_router(mutasi.router)
