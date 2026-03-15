from fastapi import FastAPI
from .routes.cases import router as cases_router

app = FastAPI(title="E-Jagriti Case API")

app.include_router(cases_router)