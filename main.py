from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.routes import main
app = FastAPI(
    title="Laporan Kepegawaian"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.api_router)
