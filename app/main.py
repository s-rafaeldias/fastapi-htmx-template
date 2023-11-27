from app import models
from app import database as db
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
import databases

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DATABASE_URL = "sqlite:///./test.db"
db_conn = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await db_conn.connect()
    await db.init_db(db_conn)


@app.on_event("shutdown")
async def shutdown():
    await db_conn.execute("DROP TABLE items")
    await db_conn.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/data", response_class=HTMLResponse)
async def data(request: Request):
    results = await db_conn.fetch_all("SELECT * FROM items")
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
    await db.insert(item=item, db=db_conn)

    results = await db_conn.fetch_all("SELECT * FROM items")
    data = [{"name": name} for _, name in results]

    return templates.TemplateResponse(
        "data.html", context={"request": request, "data": data}
    )
