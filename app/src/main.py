from fastapi import FastAPI
from src.routers import organizations, buildings
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get('/')
def get_root():
    return RedirectResponse(url=app.docs_url)


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

# poetry run uvicorn src.main:app --reload
