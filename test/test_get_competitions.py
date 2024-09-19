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
    conn.execute('CREATE TABLE IF NOT EXISTS player_seasons_data ("Player Name" TEXT, Tournament TEXT)')
    conn.execute('INSERT INTO player_seasons_data ("Player Name", Tournament) VALUES ("Lionel Messi", "La Liga")')
    conn.commit()
    return conn

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    monkeypatch.setattr('your_flask_app.get_db_connection', mock_get_db_connection)

def test_get_competitions(client):
    response = client.get('/api/competitions', query_string={'player_name': 'Lionel Messi'})
    assert response.status_code == 200
    data = response.get_json()
    assert data == ['La Liga']

def test_get_competitions_no_player(client):
    response = client.get('/api/competitions', query_string={'player_name': 'Unknown Player'})
    assert response.status_code == 200
    data = response.get_json()
    assert data == []
