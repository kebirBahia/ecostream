"""Traitement batch PySpark - Calcul des KPIs e-commerce"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as _sum, avg, count, when
)


def create_spark_session():
    return SparkSession.builder \
        .appName("EcoStream-Batch") \
        .getOrCreate()


def compute_kpis(spark, input_path):
    """Calcule les KPIs e-commerce à partir du CSV"""
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Nettoyage
    df = df.dropna(subset=['price', 'quantity'])
    df = df.filter(col('price') > 0)
    df = df.filter(col('quantity') > 0)

    # KPIs par produit
    kpis = df.groupBy('product_id', 'category').agg(
        _sum('price').alias('total_revenue'),
        _sum('quantity').alias('total_quantity'),
        count('order_id').alias('total_orders'),
        avg('price').alias('avg_price')
    )

    # Taux d'annulation par produit
    cancel = df.groupBy('product_id').agg(
        (count(when(col('status') == 'cancelled', 1)) / count('*'))
        .alias('cancel_rate')
    )

    final = kpis.join(cancel, on='product_id')
    return final


def global_kpis(spark, input_path):
    """KPIs globaux (tous produits confondus)"""
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    df = df.filter(col('status') == 'completed')

    return {
        'total_revenue': df.agg(_sum('price')).collect()[0][0],
        'total_orders': df.count(),
        'avg_cart': df.agg(avg('price')).collect()[0][0]
    }


def main():
    spark = create_spark_session()
    print("📊 Calcul des KPIs par produit...")
    kpis = compute_kpis(spark, '/data/historical_orders.csv')
    kpis.show(20)

    print("\n📈 KPIs globaux :")
    globals_kpi = global_kpis(spark, '/data/historical_orders.csv')
    for key, value in globals_kpi.items():
        print(f"  {key} = {value}")

    spark.stop()


if __name__ == '__main__':
    main()