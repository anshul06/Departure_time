from fastapi import FastAPI
from app.routes.departures import router

app = FastAPI(title="Departure Times API")

app.include_router(router)
