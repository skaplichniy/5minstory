from airtable import Airtable
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from random import randrange
from dotenv import load_dotenv
import os

load_dotenv()
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
API_KEY = os.getenv('API_KEY')
# OFFSET = os.getenv('OFFSET')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

params = ()
airtable_records = []
run = True


def get_story(n=None):
    at = Airtable(BASE_ID, API_KEY)
    response = at.get(TABLE_NAME, view='Main View')
    airtable_response = response.get('records')
    if n is None:
        n = randrange(99)
    key_story = {
        'title': airtable_response[n]['fields']['title'],
        'author': airtable_response[n]['fields']['author'],
        'story': airtable_response[n]['fields']['story'],
    }
    return key_story


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    key_story = get_story()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "story": key_story.get('story'),
            "title": key_story.get('title'),
            "author": key_story.get('author'),
        })


@app.get("/{number}", response_class=HTMLResponse)
def page_story(request: Request, number: int):
    key_story = get_story(number)
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "story": key_story.get('story'),
            "title": key_story.get('title'),
            "author": key_story.get('author'),
        })
