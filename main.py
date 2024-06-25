from fastapi import FastAPI, Request
from scrapper import dotaBuffScrapping, heroes_links, counterBuffScrapper
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/')
def get_home(request: Request):
    return templates.TemplateResponse("home_page/home.html",
                                      {"request": request})


@app.get('/info')
def get_hero_links(request: Request):
    return templates.TemplateResponse("heroes_page/heroes.html",
                                      {"request": request,
                                       "heroes": heroes_links()})


@app.get("/info/{item_id}")
def get_hero_info(request: Request, item_id: str):
    return templates.TemplateResponse("info_page/info.html",
                                      {"request": request,
                                       "hero_name": item_id,
                                       "statistics":
                                       dotaBuffScrapping(item_id)})


@app.get("/counter/{item_id}")
def get_hero_counters(request: Request, item_id: str):
    return templates.TemplateResponse("counter_page/counter.html",
                                      {"request": request,
                                       "hero_name": item_id,
                                       "statistics":
                                       counterBuffScrapper(item_id)})
