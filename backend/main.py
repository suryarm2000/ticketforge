from fastapi import FastAPI, HTTPException

app = FastAPI()

events = [{"id": 1,
           "title": "event1",
           "venue": "venue1",
           "date": "2026-12-01",
           "price": 100}, 
           {"id": 2,
           "title": "event2",
           "venue": "venue2",
           "date": "2026-12-02",
           "price": 200},
           {"id": 3,
           "title": "event3",
           "venue": "venue3",
           "date": "2026-12-03",
           "price": 300}]

@app.get("/")
def read_root():
    return {"message": "TicketForge API"}

@app.get("/events")
def get_event_list():
    return events

@app.get("/events/{event_id}")
def get_event(event_id: int):
    for event in events:
        if event_id == event["id"]:
            return event
    raise HTTPException(status_code=404, detail="Event not found")