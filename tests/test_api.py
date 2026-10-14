"""Tests de l'API d'ingestion"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'couche2_ingestion' / 'api'))

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()['service'] == 'EcoStream API'


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_ingest_event():
    event = {
        'event_id': 'test-123',
        'user_id': 1001,
        'product_id': 201,
        'category': 'Électronique',
        'event_type': 'click',
        'price': 49.99,
        'quantity': 1,
        'timestamp': '2026-10-03T10:00:00',
        'country': 'FR'
    }
    response = client.post("/ingest/event", json=event)
    assert response.status_code == 200
    assert response.json()['status'] == 'received'
    