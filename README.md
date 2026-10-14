 # EcoStream — Pipeline de Données E-commerce

## 📝 Description

EcoStream est un pipeline de données e-commerce qui collecte, traite, stocke et analyse en temps réel et en batch les événements générés par une plateforme de vente en ligne. Le projet suit une architecture en 5 couches.

## 🏗️ Architecture

1. **Sources** : Simulateur Python + CSV + API externe
2. **Ingestion** : Kafka + FastAPI
3. **Traitement** : Spark + Flink + scikit-learn
4. **Stockage** : Cassandra + HBase
5. **Orchestration** : Apache Airflow

## 🚀 Démarrage

```bash
docker-compose up -d
