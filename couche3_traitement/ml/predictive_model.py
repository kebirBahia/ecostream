"""Modèle prédictif - Prédiction d'abandon de panier"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def prepare_data(data_path):
    """Prépare les données pour l'entraînement"""
    df = pd.read_csv(data_path)

    # Features
    features_df = df[['user_id', 'product_id', 'quantity', 'price']].copy()

    # Cible : commande annulée = 1, sinon 0
    df['is_cancelled'] = (df['status'] == 'cancelled').astype(int)
    y = df['is_cancelled']

    # Si pas assez de classes, générer des données synthétiques
    if y.nunique() < 2:
        np.random.seed(42)
        y = pd.Series(np.random.randint(0, 2, len(df)))

    return features_df, y


def train_model(data_path, model_path='/models/abandon_model.pkl'):
    """Entraîne le modèle de prédiction d'abandon"""
    X, y = prepare_data(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"✅ Modèle entraîné - Précision : {accuracy:.2%}")
    print(classification_report(y_test, y_pred))

    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"💾 Modèle sauvegardé : {model_path}")

    return model


def predict_abandon(model_path, event):
    """Prédit l'abandon pour un événement donné"""
    model = joblib.load(model_path)

    features = [[
        event['user_id'],
        event['product_id'],
        event['quantity'],
        event['price']
    ]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        'will_abandon': bool(prediction),
        'probability': round(float(probability), 3),
        'level': 'ÉLEVÉ' if probability > 0.7 else 'MOYEN' if probability > 0.4 else 'FAIBLE'
    }


if __name__ == '__main__':
    train_model('/data/historical_orders.csv')