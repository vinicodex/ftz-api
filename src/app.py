from fastapi import FastAPI
from src.apps.users.api import router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

