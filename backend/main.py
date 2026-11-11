from fastapi import FastAPI
from routers import events

app = FastAPI()
app.include_router(events.router)

@app.get("/")
def read_root():
    return {"message": "TicketForge API"}