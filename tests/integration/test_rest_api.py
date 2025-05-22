import pytest
from fastapi.testclient import TestClient
from src.pygridfight.main import app

client = TestClient(app)

def create_game_payload():
    return {
        "name": "Test Game",
        "max_players": 4,
        "grid_size": 20,
        "is_private": False
    }

def join_game_payload(name="Player1"):
    return {
        "player_name": name
    }

def leave_game_payload(player_id):
    return {
        "player_id": player_id
    }

def test_create_and_get_game():
    # Create game
    resp = client.post("/games", json=create_game_payload())
    assert resp.status_code == 201
    data = resp.json()
    assert "game" in data and "player_id" in data
    game_id = data["game"]["id"]

    # Get game
    resp = client.get(f"/games/{game_id}")
    assert resp.status_code == 200
    game = resp.json()
    assert game["id"] == game_id
    assert game["name"] == "Test Game"

def test_list_games():
    # Create a game to ensure at least one exists
    client.post("/games", json=create_game_payload())
    resp = client.get("/games")
    assert resp.status_code == 200
    data = resp.json()
    assert "games" in data
    assert data["total"] >= 1

def test_join_and_leave_game():
    # Create game
    resp = client.post("/games", json=create_game_payload())
    game_id = resp.json()["game"]["id"]

    # Join game
    resp = client.post(f"/games/{game_id}/join", json=join_game_payload("Alice"))
    assert resp.status_code == 200
    join_data = resp.json()
    assert "player_id" in join_data
    player_id = join_data["player_id"]

    # Leave game
    resp = client.request("DELETE", f"/games/{game_id}/leave", json=leave_game_payload(player_id))
    assert resp.status_code == 200
    leave_data = resp.json()
    assert "message" in leave_data

def test_delete_game():
    # Create game
    resp = client.post("/games", json=create_game_payload())
    game_id = resp.json()["game"]["id"]

    # Delete game
    resp = client.delete(f"/games/{game_id}")
    assert resp.status_code == 204

    # Ensure game is gone
    resp = client.get(f"/games/{game_id}")
    assert resp.status_code == 404

def test_join_full_game():
    # Create game with 2 max players
    payload = create_game_payload()
    payload["max_players"] = 2
    resp = client.post("/games", json=payload)
    game_id = resp.json()["game"]["id"]

    # Join with two players
    client.post(f"/games/{game_id}/join", json=join_game_payload("P1"))
    client.post(f"/games/{game_id}/join", json=join_game_payload("P2"))

    # Third join should fail
    resp = client.post(f"/games/{game_id}/join", json=join_game_payload("P3"))
    assert resp.status_code == 400

def test_join_nonexistent_game():
    resp = client.post("/games/doesnotexist/join", json=join_game_payload("Ghost"))
    assert resp.status_code == 404

def test_leave_nonexistent_game():
    resp = client.request("DELETE", "/games/doesnotexist/leave", json=leave_game_payload("ghostid"))
    assert resp.status_code == 404

def test_delete_nonexistent_game():
    resp = client.delete("/games/doesnotexist")
    assert resp.status_code == 404

def test_create_game_invalid_payload():
    # Missing name
    payload = create_game_payload()
    del payload["name"]
    resp = client.post("/games", json=payload)
    assert resp.status_code == 422

def test_join_game_invalid_payload():
    # Missing player_name
    resp = client.post("/games/someid/join", json={})
    assert resp.status_code == 422

def test_leave_game_invalid_payload():
    # Missing player_id
    resp = client.request("DELETE", "/games/someid/leave", json={})
    assert resp.status_code == 422