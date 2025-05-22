from fastapi import FastAPI
from src.routers import organizations, buildings, web
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get('/')
def get_root():
    return RedirectResponse(url='/organizations')


app.include_router(
    organizations.router,
    prefix='/organizations',
    tags=['organizations']
)
app.include_router(
    buildings.router,
    prefix='/buildings',
    tags=['buildings']
)
app.include_router(web.router)

# poetry run uvicorn src.main:app --reload
