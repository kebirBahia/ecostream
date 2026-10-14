"""Producteur Kafka pour import batch de CSV"""
import json
import csv
from kafka import KafkaProducer


def send_csv_to_kafka(csv_path, topic='ecommerce-events'):
    """Envoie les lignes d'un CSV vers Kafka"""
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            producer.send(topic, value=row)
            count += 1

    producer.flush()
    producer.close()
    print(f"✅ {count} lignes envoyées vers Kafka")
    return count


if __name__ == '__main__':
    send_csv_to_kafka('/data/historical_orders.csv')