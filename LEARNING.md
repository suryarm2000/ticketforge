# Learning log

One entry per day: what I built, what I learned, what is still unclear.

## 2026-10-29 (Day 1)

- Built: created the repo and project skeleton.
- Learned: project plan and stack (React, FastAPI, PostgreSQL).
- 404 and 422 errors: 404 - the thing you asked for does not exist, 422 - bad input
- --reload: reloads each time when changes happens in code
- GET reads data and should not change anything. POST sends data to create something

## 2026-10-30 (Day 2)

- Built: POST /events (create) and PUT /events/{id} (update), plus the EventCreate Pydantic model.
- Pydantic model: a class that describes what data should look like (field names and types). FastAPI uses it to check incoming JSON automatically and returns 422 if it doesn't match.
- BaseModel: Pydantic's starting class; my class inherits it to get validation for free.
- model_dump(): turns a Pydantic object back into a normal dictionary so I can add the id.
- POST returns 201 (Created), a successful create; GET/PUT return 200 (OK).
- PUT replaces an existing event with the whole new data; the id comes from the URL so it can't be changed.
- Path parameter vs request body: event_id comes from the URL, event comes from the JSON body. FastAPI tells them apart by itself.
- Unclear / problems:
  - New ids use max(ids) + 1. If I delete the highest-id event, the next new event reuses that id. A database auto-increment id fixes this.
  - Two requests arriving at the same moment could both get the same new id.
  - date is just text, so "31-10-2026" and "2026-12-01" are both accepted. Need a real date type.
  - Negative prices are accepted.
  - Data lives in a Python list, so it is lost when the server restarts. This is why I need a database.