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

## 2026-11-06 (Day 3)

- Pydantic model describes the shape of the data (which field exists and their types)
- model_dump() converts a pydantic object into a normal python dictionary 
- A database’s auto-increment counter only goes up, so ids are never reused even after deletes.
- Added delete endpoint which has status code 204 - which means no content but request is success
- datetime.data is YYYY-MM-DD format
- model_dump(mode="json") tells pydantic to covert special data types into a JSON friendly values so that the date becomes a string

## 2026-11-11 (Day 4)

- Built: finished Phase 1. Split the single main.py into main.py (creates the app), schemas.py (Pydantic models) and routers/events.py (all /events routes). Added pytest tests in test_events.py.
- Router: APIRouter groups routes in their own file. prefix="/events" adds /events to every route in it, so decorators use "" and "/{event_id}". main.py plugs it in with app.include_router(...).
- Package: a folder with __init__.py is importable as a package (routers).
- pytest: finds test_*.py files and runs functions starting with test_. assert passes if the value is true and fails the test if not. TestClient (needs httpx) calls the API in memory without starting uvicorn.
- f-string: f"/events/{event_id}" puts the variable's value into the text.
- AttributeError: the object has no such method/value. My bug was client.update(...) instead of client.put(...). Reading the last line of pytest's failure output pointed straight at it.
- 3 tests pass: full create/get/update/delete lifecycle, bad price gives 422, unknown event gives 404.
- Phase 2 concepts (read, not built yet): a database stores data on disk so it survives restarts. Table = list of similar records, row = one record, column = one field with a type, primary key = unique id per row. SQL is the language to query it: SELECT, INSERT, UPDATE, DELETE match GET, POST, PUT, DELETE.
- Docker: runs programs in isolated containers made from images. A volume keeps data outside the container so it survives deleting it. -p 5432:5432 connects my machine's port to Postgres inside the container.
- Unclear / to do:
  - I have only read the test code once. Need to re-read test_events.py and be able to explain each line.
  - Haven't started the Postgres container yet.
  - The events list still resets whenever the server restarts.