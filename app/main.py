from fastapi import FastAPI
from app.routes.departures import router
from fastapi.responses import RedirectResponse


app = FastAPI(title="Departure Times API")

app.include_router(router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
