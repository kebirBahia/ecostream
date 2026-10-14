"""
Simulateur d'événements e-commerce en temps réel.
Génère des clics, ajouts au panier et commandes.
"""
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer


EVENT_TYPES = ['click', 'add_to_cart', 'purchase', 'view_product']
CATEGORIES = ['Électronique', 'Vêtements', 'Livres', 'Maison', 'Sport']
COUNTRIES = ['FR', 'DZ', 'MA', 'TN', 'US', 'DE', 'ES', 'IT']


def generate_event():
    """Génère un événement e-commerce aléatoire"""
    event_type = random.choices(
        EVENT_TYPES,
        weights=[50, 25, 15, 10]
    )[0]

    return {
        'event_id': f"evt-{random.randint(100000, 999999)}",
        'user_id': random.randint(1000, 9999),
        'product_id': random.randint(100, 500),
        'category': random.choice(CATEGORIES),
        'event_type': event_type,
        'price': round(random.uniform(5.0, 500.0), 2),
        'quantity': random.randint(1, 5),
        'timestamp': datetime.utcnow().isoformat(),
        'country': random.choice(COUNTRIES)
    }


def connect_to_kafka(max_retries=60, delay=5):
    """Tente de se connecter à Kafka avec retry (max 5 minutes)"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔄 Tentative {attempt}/{max_retries} - Connexion à Kafka...", flush=True)
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=10000,
                api_version_auto_timeout_ms=10000
            )
            print("✅ Connecté à Kafka avec succès !", flush=True)
            return producer
        except Exception as e:
            print(f"⚠️ Kafka pas prêt ({type(e).__name__}) - Attente {delay}s...", flush=True)
            time.sleep(delay)
    return None


def main():
    """Point d'entrée du simulateur"""
    print("🛒 EcoStream Simulator — Démarrage", flush=True)
    print(f"📊 Types d'événements : {EVENT_TYPES}", flush=True)

    producer = connect_to_kafka()

    if producer is None:
        print("❌ Impossible de se connecter à Kafka après 5 minutes", flush=True)
        return

    print("🚀 Démarrage de l'envoi d'événements...", flush=True)
    count = 0

    try:
        while True:
            event = generate_event()
            producer.send('ecommerce-events', value=event)
            count += 1

            if count % 100 == 0:
                print(f"📤 {count} événements envoyés", flush=True)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n⏹️ Arrêt. Total : {count} événements", flush=True)
    finally:
        producer.close()


if __name__ == '__main__':
    main()
    