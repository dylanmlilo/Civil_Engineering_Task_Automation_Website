from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import beams, sewer
from .utils.templates import templates
import os

app = FastAPI(
    title="Civil Engineering Calculator API",
    description="API for civil engineering calculations",
    version="0.1.0"
)

# Get absolute path to templates
current_dir = os.path.dirname(os.path.abspath(__file__))

# Static files
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")


app.include_router(beams.router)
app.include_router(sewer.router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/beams")
async def render_beam_page(request: Request):
    return templates.TemplateResponse("beams.html", {"request": request})

@app.get("/sewer")
async def render_sewer_page(request: Request):
    return templates.TemplateResponse("sewer.html", {"request": request})

@app.get("/test_sewer")
async def rebder_test_sewer_page(request: Request):
    return templates.TemplateResponse("test_sewer.html", {"request": request})