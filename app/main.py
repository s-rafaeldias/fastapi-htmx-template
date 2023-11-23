from app import models
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DATA = [
    {"name": "Rafael"},
    {"name": "Dias"},
    {"name": "Silveira"},
]


@app.get("/data", response_class=HTMLResponse)
async def data(request: Request):
    return templates.TemplateResponse(
        "data.html", context={"request": request, "data": DATA}
    )


@app.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse(
        "form.html", context={"request": request, "item_type": models.ItemType}
    )


@app.post("/form", response_class=HTMLResponse)
async def add_data(request: Request, item: models.ItemForm = Depends()):
    # DATA.append({"name": name})
    print(item)
    return templates.TemplateResponse(
        "data.html", context={"request": request, "data": DATA}
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
