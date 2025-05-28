from fastapi import APIRouter


from . import dnp, duk, so, statistik, mutasi, kontrak, lepas_tanggungan_anak, kenaikan_berkala
api_router = APIRouter()

api_router.include_router(duk.router)
api_router.include_router(dnp.router)
api_router.include_router(so.router)
api_router.include_router(statistik.router)
api_router.include_router(mutasi.router)
api_router.include_router(kontrak.router)
api_router.include_router(lepas_tanggungan_anak.router)
api_router.include_router(kenaikan_berkala.router)

