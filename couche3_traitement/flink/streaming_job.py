"""Traitement streaming Flink - Détection d'événements en temps réel"""
import json


def parse_event(raw_message):
    """Parse un événement JSON"""
    data = json.loads(raw_message)
    return {
        'event_id': data['event_id'],
        'user_id': data['user_id'],
        'product_id': data['product_id'],
        'event_type': data['event_type'],
        'price': data['price'],
        'timestamp': data['timestamp']
    }


def detect_high_value_purchase(event):
    """Détecte les achats à forte valeur (> 300€)"""
    if event['event_type'] == 'purchase' and event['price'] > 300:
        return {
            'alert_type': 'HIGH_VALUE_PURCHASE',
            'event_id': event['event_id'],
            'user_id': event['user_id'],
            'price': event['price']
        }
    return None


def detect_cart_abandonment(events_window):
    """
    Détecte l'abandon de panier :
    add_to_cart suivi d'aucun purchase dans la fenêtre
    """
    users_with_cart = set()
    users_with_purchase = set()

    for e in events_window:
        if e['event_type'] == 'add_to_cart':
            users_with_cart.add(e['user_id'])
        elif e['event_type'] == 'purchase':
            users_with_purchase.add(e['user_id'])

    abandoned = users_with_cart - users_with_purchase
    return [
        {'alert_type': 'CART_ABANDONED', 'user_id': uid}
        for uid in abandoned
    ]


if __name__ == '__main__':
    sample_events = [
        {'event_id': 'e1', 'user_id': 1001, 'product_id': 201,
         'event_type': 'purchase', 'price': 450.0, 'timestamp': 'now'},
        {'event_id': 'e2', 'user_id': 1002, 'product_id': 202,
         'event_type': 'add_to_cart', 'price': 30.0, 'timestamp': 'now'},
    ]

    for e in sample_events:
        alert = detect_high_value_purchase(e)
        if alert:
            print(f"🚨 Alerte : {alert}")

    abandoned = detect_cart_abandonment(sample_events)
    print(f"🛒 Paniers abandonnés : {abandoned}")