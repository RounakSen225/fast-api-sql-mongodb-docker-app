from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_player = {
  "birthYear": 1981,
  "birthMonth": 12,
  "birthDay": 27,
  "birthCountry": "USA",
  "birthState": "CO",
  "birthCity": "Denver",
  "deathYear": None,
  "deathMonth": None,
  "deathDay": None,
  "nameFirst": "David",
  "nameLast": "Aardsma",
  "nameGiven": "David Allan",
  "weight": 215,
  "height": 75,
  "bats": "R",
  "throws": "R",
  "debut": "2004-04-06",
  "finalGame": "2015-08-23",
  "retroID": "aardd001",
  "bbrefID": "aardsda01"
}

created_playerID = None

def test_get_players():
    response = client.get("/api/players", headers={"token": "user1"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_player():
    response = client.get("/api/players/aasedo01", headers={"token": "user1"})
    assert response.status_code == 200
    assert "playerID" in response.json()

def test_player_not_found():
    response = client.get("/api/players/1111111", headers={"token": "user1"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}

def test_invalid_user():
    response = client.get("/api/players/999", headers={"token": "user10"})
    assert response.status_code == 401
    print(response.json())
    assert response.json() == {"detail": "Invalid authentication credentials"}

def test_create_player():
    global created_playerID
    response = client.post(
        "/api/players/",
        json=test_player
    )
    assert response.status_code == 200
    data = response.json()
    created_playerID = data["playerID"]

def test_update_player():
    global created_playerID
    url = "/api/players/" + created_playerID
    # Assuming you have a player with ID 1
    response = client.put(
        url,
        json=test_player
    )
    assert response.status_code == 200

def test_delete_player():
    global created_playerID
    url = "/api/players/" + created_playerID
    response = client.delete(url)
    assert response.status_code == 200

    # Try to get the deleted player
    response = client.get(url, headers={"token": "user1"})
    assert response.status_code == 404