from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / 'templates')


@router.get('/buildings', response_class=HTMLResponse)
async def show_buildings_page(request: Request):
    return templates.TemplateResponse(
        'buildings.html', {'request': request}
    )


@router.get('/organizations', response_class=HTMLResponse)
async def show_organizations_page(request: Request):
    return templates.TemplateResponse(
        'organizations.html', {'request': request}
    )


@router.get('/activities', response_class=HTMLResponse)
async def show_activities_page(request: Request):
    return templates.TemplateResponse(
        'activities.html', {'request': request}
    )
