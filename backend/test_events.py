from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_event_lifecycle():
    new_event = {
        "title": "Test Show",
        "venue": "Test Hall",
        "date": "2026-12-25",
        "price": 250
    }

    created = client.post("/events", json=new_event)
    assert created.status_code == 201
    event_id = created.json()["id"]

    fetched = client.get(f"/events/{event_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Test Show"

    updated = client.put(f"/events/{event_id}", json={**new_event, "price": 300})
    assert updated.status_code == 200
    assert updated.json()["price"] == 300

    deleted = client.delete(f"/events/{event_id}")
    assert deleted.status_code == 204
    assert client.get(f"/events/{event_id}").status_code == 404

def test_rejects_bad_price():
    bad = {"title": "X", "venue": "Y", "date": "2026-12-25", "price": -5}
    assert client.post("/events", json=bad).status_code == 422

def test_unknown_event_is_404():
    assert client.get("/events/99999").status_code == 404