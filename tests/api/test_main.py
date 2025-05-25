import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from fastapi.testclient import TestClient
from pygridfight.main import app

client = TestClient(app)

def test_create_game_endpoint():
    response = client.post(
        "/api/v1/game",
        json={
            "player_display_name": "Test Player",
            "grid_size": 8,
            "target_score": 50
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "IN_PROGRESS"
    assert data["grid"]["size"] == 8
    assert data["players"][0]["display_name"] == "Test Player"
    assert len(data["grid"]["cells"]) == 8 * 8
    # Check that at least one cell has a resource (initial resources spawned)
    resource_cells = [
        cell for cell in data["grid"]["cells"].values()
        if cell.get("resource") is not None
    ]
    assert len(resource_cells) > 0