from fastapi import FastAPI
from app.api.v1.endpoints import router

app = FastAPI(
    title="Ctypto Futures Data API",
    version="1.0.0",
)

app.include_router(router=router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Crypto Futures Data API"}
