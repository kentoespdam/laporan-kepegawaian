from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
from app.routes import main

app = FastAPI(
    title="Laporan Kepegawaian"
)

# laporan_kepegawaian.mount("/public", StaticFiles(directory="static/public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.api_router)
