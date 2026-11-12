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
- Docker: runs programs in isolated containers made from images. A volume keeps data outside the container so it survives deleting it.
- Unclear / to do:
  - I have only read the test code once. Need to re-read test_events.py and be able to explain each line.
  - The events list still resets whenever the server restarts.

## 2026-11-12 (Day 5)

- Module vs package: a module is one .py file (events.py). A package is a folder of modules with an __init__.py (routers).
- f-string vs path template: "/{event_id}" in a FastAPI decorator is a plain string that FastAPI reads as a template ("this part of the URL is the variable event_id"). In the tests I build a real URL, so I need f"/events/{event_id}" to put the actual value in. Without the f the literal text {event_id} would be sent and give a 422 (cannot parse as integer), not a 404.
- APIRouter(prefix, tags): prefix is added to the start of every route path in that router, so it changes the real URLs. tags only groups routes under a heading in /docs and does not change behaviour.
- __init__.py in routers: marks the folder as a package so "from routers import events" works. Python can sometimes import without it (namespace packages) but it is the convention and tools like pytest expect it. It is only needed in routers because that is the only folder I import from as a package.
- test_events.py walkthrough: TestClient(app) calls the API in memory. client.post/get/put/delete return a response; .status_code is the number, .json() turns the body into a dictionary. Each assert is a checkpoint and the test fails at the first false one.
  - test_event_lifecycle: create, read, update, delete, then confirm 404. One long test because each step needs the previous one, and it deletes what it creates.
  - test_rejects_bad_price: price -5 gives 422. If I removed gt=0, this test would fail because the API would reply 201.
  - test_unknown_event_is_404: event 99999 gives 404.
- Why event_id is saved in the lifecycle test: the server assigns the id on create, and I need it to fetch, update and delete that same event.
- Database concepts (Phase 2, part 1): a table is a named grid for one kind of thing (events), a column is one field with a fixed type, a row is one record, and the primary key (id) is unique per row. Constraints like NOT NULL are rules the database itself enforces, so bad data is refused even if my Python code has a bug (Pydantic guards the front door, constraints guard the vault).
- SQL: SELECT (read, like GET), INSERT (create, like POST), UPDATE (like PUT), DELETE (like DELETE). WHERE filters rows, * means all columns.
- Relational: tables are linked with foreign keys, for example a booking stores the id of its event.
- SQLite vs PostgreSQL: SQLite is a single file with no server, good for small apps (used at bgx). PostgreSQL is a separate server that handles many users safely and is what production apps and job postings use.
- Unclear / to do:
  - Have not run the hands-on SQLite experiment yet (create table, insert, select, delete, see that ids are never reused, see NOT NULL refuse a row).
  - Postgres container in Docker is not started yet.