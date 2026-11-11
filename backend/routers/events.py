from fastapi import APIRouter, HTTPException
from schemas import EventCreate

router = APIRouter(prefix="/events", tags=["events"])

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


@router.get("")
def get_event_list():
    return events

@router.get("/{event_id}")
def get_event(event_id: int):
    for event in events:
        if event_id == event["id"]:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.post("", status_code=201)
def create_event(event: EventCreate):
    ids = [e["id"] for e in events]
    new_id = max(ids, default=0) + 1
    new_event = {"id": new_id, **event.model_dump(mode="json")}
    events.append(new_event)
    return new_event

@router.put("/{event_id}")
def update_event(event_id: int, event: EventCreate):
    for index, existing in enumerate(events):
        if existing["id"] == event_id:
            updated = {"id": event_id, **event.model_dump(mode="json")}
            events[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int):
    for index, existing in enumerate(events):
        if existing["id"] == event_id:
            events.pop(index)
            return
    raise HTTPException(status_code=404, detail="Event not found")