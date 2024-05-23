from fastapi import FastAPI
from backend.src.pc.router import router as pc_router
from backend.src.ps.router import router as ps_router
from backend.src.vr.router import router as vr_router

app = FastAPI()
app.include_router(pc_router)
app.include_router(ps_router)
app.include_router(vr_router)
