import pytest
from fastapi.testclient import TestClient
from pygridfight.main import app

client = TestClient(app)

def test_health_check_details():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "pygridfight"
    assert "timestamp" in data
    assert "system" in data
    assert "config" in data
    assert "python_version" in data["system"]
    assert "host" in data["config"]

def test_cors_headers():
    resp = client.options("/health", headers={"Origin": "http://testclient"})
    assert "access-control-allow-origin" in resp.headers

def test_openapi_docs():
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.json()
    assert data["info"]["title"] == "PyGridFight"

def test_request_id_header():
    resp = client.get("/health")
    assert "x-request-id" in resp.headers

def test_game_error_handler(monkeypatch):
    from pygridfight.core.exceptions import GameError

    @app.get("/raise-game-error")
    async def raise_game_error():
        raise GameError("test game error")

    resp = client.get("/raise-game-error")
    assert resp.status_code == 400
    assert resp.json()["error"] == "GameError"

def test_player_error_handler(monkeypatch):
    from pygridfight.core.exceptions import PlayerError

    @app.get("/raise-player-error")
    async def raise_player_error():
        raise PlayerError("test player error")

    resp = client.get("/raise-player-error")
    assert resp.status_code == 400
    assert resp.json()["error"] == "PlayerError"