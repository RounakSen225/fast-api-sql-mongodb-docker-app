# tests/test_main.py

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.models import ScoreDB

client = TestClient(app)

@pytest.mark.asyncio
@patch('app.crud.get_top_scores', new_callable=AsyncMock)
async def test_get_top_scores(mock_get_top_scores):
    mock_get_top_scores.return_value = [
        ScoreDB(player_name="Alice", score=2000).dict(),
        ScoreDB(player_name="Bob", score=1800).dict(),
    ]
    response = client.get("/top-scores/", headers={"token":"user1"})
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) == 5

@pytest.mark.asyncio
@patch('app.crud.insert_score', new_callable=AsyncMock)
async def test_create_score(mock_create_score):
    mock_create_score.return_value = ScoreDB(player_name="Alice", score=2000).dict()
    response = client.post("/scores", headers={"token":"user1"}, json={"player_name": "Alice", "score": 2000})
    assert response.status_code == 200
    assert response.json()["player_name"] == "Alice"
    assert response.json()["score"] == 2000

@pytest.mark.asyncio
@patch('app.crud.update_score', new_callable=AsyncMock)
async def test_update_score(mock_update_score):
    mock_update_score.return_value = True
    score_id = "60e2f9e2f8e4e2b1e8b3b2a9"
    response = client.put(f"/scores/{score_id}", headers={"token":"user1"},  json={"player_name": "Alice", "score": 2100})
    assert response.status_code == 200
    assert "Score updated successfully" in response.text

@pytest.mark.asyncio
@patch('app.crud.delete_score', new_callable=AsyncMock)
async def test_delete_score(mock_delete_score):
    mock_delete_score.return_value = True
    score_id = "60e2f9e2f8e4e2b1e8b3b2a9"
    response = client.delete(f"/scores/{score_id}", headers={"token":"user1"})
    assert response.status_code == 200
    assert "Score deleted successfully" in response.text

@pytest.mark.asyncio
@patch('app.crud.delete_score', new_callable=AsyncMock)
async def test_delete_score_not_found(mock_delete_score):
    mock_delete_score.return_value = False
    score_id = "60e2f9e2f8e4e2b1e8b3b2a9"
    response = client.delete(f"/scores/{score_id}", headers={"token":"user1"})
    assert response.status_code == 404
    assert "Score not found" in response.text