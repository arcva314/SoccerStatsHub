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
    conn.execute('CREATE TABLE IF NOT EXISTS manager_seasons_data ("Name" TEXT, "Wins" INTEGER)')
    conn.commit()
    return conn

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    monkeypatch.setattr('your_flask_app.get_db_connection', mock_get_db_connection)

def test_get_manager_stats(client):
    response = client.get('/api/manager_stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'Name' not in data
    assert 'Wins' in data
