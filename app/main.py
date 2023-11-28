from app import models
from app import database as db
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
import databases

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DATABASE_URL = "sqlite:///./test.db"
DB_CONN = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await DB_CONN.connect()
    await db.init_db(DB_CONN)


@app.on_event("shutdown")
async def shutdown():
    await DB_CONN.execute("DROP TABLE items")
    await DB_CONN.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/data", response_class=HTMLResponse)
async def data(request: Request):
    results = await DB_CONN.fetch_all("SELECT * FROM items")
    data = [{"name": name} for _, name in results]

    return templates.TemplateResponse(
        "data.html", context={"request": request, "data": data}
    )


@app.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse(
        "form.html", context={"request": request, "item_type": models.ItemType}
    )


@app.post("/form", response_class=HTMLResponse)
async def add_data(request: Request, item: models.ItemForm = Depends()):
    await db.insert(item=item, db=DB_CONN)

    results = await DB_CONN.fetch_all("SELECT * FROM items")
    data = [{"name": name} for _, name in results]

    return templates.TemplateResponse(
        "data.html", context={"request": request, "data": data}
    )
