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


## 📸 Captures d'écran — Preuves de fonctionnement

### Dépôt GitHub
![GitHub](docs/01-github-repo.png)

### Pipeline CI/CD
![GitHub Actions](docs/02-github-actions.png)

### Services Docker
![Docker](docs/03-docker-ps.png)

### Simulateur en fonctionnement
![Simulator](docs/04-simulator-logs.png)

### API Swagger
![API](docs/05-api-swagger.png)

### Airflow DAGs
![Airflow](docs/06-airflow-dags.png)

### HBase UI
![HBase](docs/07-hbase-ui.png)

### Tests automatisés
![Tests](docs/08-tests-pytest.png)
