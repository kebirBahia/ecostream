"""API FastAPI pour ingestion des événements e-commerce"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from datetime import datetime
import csv
import io

app = FastAPI(title="EcoStream Ingestion API", version="1.0.0")


class Event(BaseModel):
    event_id: str
    user_id: int
    product_id: int
    category: str
    event_type: str
    price: float
    quantity: int
    timestamp: str
    country: str


@app.get("/")
def root():
    return {"service": "EcoStream API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/ingest/event")
def ingest_event(event: Event):
    """Ingère un événement unique"""
    print(f"📥 Événement reçu : {event.event_id} ({event.event_type})")
    return {"status": "received", "event_id": event.event_id}


@app.post("/ingest/batch")
async def ingest_batch(file: UploadFile = File(...)):
    """Ingère un fichier CSV en batch"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Le fichier doit être un CSV")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))
    rows = list(reader)

    return {
        "status": "processed",
        "filename": file.filename,
        "rows_ingested": len(rows),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/kpis/summary")
def get_kpis_summary():
    """Retourne un résumé des KPIs (exemple)"""
    return {
        'total_revenue': 12345.67,
        'total_orders': 456,
        'avg_cart': 27.08,
        'conversion_rate': 0.035
    }