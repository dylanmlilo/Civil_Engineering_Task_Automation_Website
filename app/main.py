from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers import beams

app = FastAPI(
    title="Civil Engineering Calculator API",
    description="API for civil engineering calculations starting with beam sizing",
    version="0.1.0"
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(beams.router)


@app.get("/")
async def home():
    return FileResponse("app/static/index.html")