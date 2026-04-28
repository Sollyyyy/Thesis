def test_get_airports(client):
    res = client.get("/api/airports")
    assert res.status_code == 200
    airports = res.json()
    assert len(airports) > 0
    assert "code" in airports[0]
    assert "city" in airports[0]
    assert "name" in airports[0]
    assert "country" in airports[0]


def test_search_unauthenticated(client):
    res = client.post("/api/search", json={
        "departure": "BUD",
        "departureCity": "Budapest",
        "destination": "BER",
        "destinationCity": "Berlin",
        "departDate": "2026-05-15"
    })
    assert res.status_code == 200
    data = res.json()
    assert "flight" in data
    assert "bus" in data
    assert "train" in data


def test_search_saves_history(client, auth_header):
    res = client.post("/api/search", json={
        "departure": "BUD",
        "departureCity": "Budapest",
        "destination": "BER",
        "destinationCity": "Berlin",
        "departDate": "2026-05-15"
    }, headers=auth_header)
    assert res.status_code == 200

    # Check history was saved
    history = client.get("/api/history", headers=auth_header)
    assert history.status_code == 200
    assert len(history.json()) > 0
    assert history.json()[0]["departure"] == "Budapest"


def test_history_no_auth(client):
    res = client.get("/api/history")
    assert res.status_code == 401
