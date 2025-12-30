from fastapi import FastAPI
from app.frameworks.api import router

app = FastAPI()
app.include_router(router)
