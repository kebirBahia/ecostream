"""Tests du simulateur"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'couche1_sources'))

from simulator import generate_event, EVENT_TYPES, CATEGORIES  # noqa: E402


def test_generate_event():
    event = generate_event()
    assert 'event_id' in event
    assert event['event_type'] in EVENT_TYPES
    assert event['category'] in CATEGORIES
    assert event['price'] > 0
    assert event['quantity'] >= 1


def test_event_structure():
    event = generate_event()
    required = [
        'event_id', 'user_id', 'product_id', 'category',
        'event_type', 'price', 'quantity', 'timestamp', 'country'
    ]
    for field in required:
        assert field in event
        