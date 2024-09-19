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
    conn.execute('CREATE TABLE IF NOT EXISTS manager_seasons_data ("Name" TEXT)')
    conn.execute('INSERT INTO manager_seasons_data ("Name") VALUES ("Pep Guardiola")')
    conn.commit()
    return conn

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    monkeypatch.setattr('your_flask_app.get_db_connection', mock_get_db_connection)

def test_get_managers(client):
    response = client.get('/api/managers')
    assert response.status_code == 200
    data = response.get_json()
    assert data == ['Pep Guardiola']

def test_get_managers_empty(client):
    conn = mock_get_db_connection()
    conn.execute('DELETE FROM manager_seasons_data')
    conn.commit()
    response = client.get('/api/managers')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []
