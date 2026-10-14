#!/bin/bash
# Initialisation des tables HBase pour EcoStream

echo "🚀 Création des tables HBase..."

echo "create 'events_aggregated', 'stats', 'meta'" | hbase shell -n
echo "create 'kpis', 'revenue', 'orders', 'dates'" | hbase shell -n
echo "create 'predictions', 'risk', 'details'" | hbase shell -n

echo "✅ Tables HBase créées avec succès"