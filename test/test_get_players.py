import pytest
import sqlite3
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def mock_get_db_connection():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute('CREATE TABLE IF NOT EXISTS player_seasons_data ("Player Name" TEXT)')
    conn.execute('INSERT INTO player_seasons_data ("Player Name") VALUES ("Lionel Messi")')
    conn.commit()
    return conn

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    monkeypatch.setattr('your_flask_app.get_db_connection', mock_get_db_connection)

def test_get_players(client):
    response = client.get('/api/players')
    assert response.status_code == 200
    data = response.get_json()
    assert data == ['Lionel Messi']

def test_get_players_empty(client):
    conn = mock_get_db_connection()
    conn.execute('DELETE FROM player_seasons_data')
    conn.commit()
    response = client.get('/api/players')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []
