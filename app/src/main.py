from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


# poetry run uvicorn src.main:app --reload
