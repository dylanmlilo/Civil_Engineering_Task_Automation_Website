from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import beams


app = FastAPI(
    title="Civil Engineering Calculator API",
    description="API for civil engineering calculations starting with beam sizing",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(beams.router)


templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})