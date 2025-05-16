# src/aggregate.py
from datetime import datetime
from src.spark_utils import create_spark_session
from src.config import SILVER_PATH, GOLD_PATH


def aggregate_to_gold(execution_date: str) -> bool:
    """
    Agrega os dados da Silver contando quantidade por tipo e estado,
    salvando particionado na camada Gold em formato Delta.

    :param execution_date: Data de execução no formato YYYYMMDD
    :return: True se sucesso
    :raises: ValueError se o caminho Silver estiver mal definido
    """
    print("🔹 Iniciando agregação dos dados (Silver ➝ Gold)")

    if not SILVER_PATH or not SILVER_PATH.startswith("s3a://"):
        raise ValueError(f"❌ SILVER_PATH inválido ou não absoluto: '{SILVER_PATH}'")

    spark = create_spark_session("AggregateGold")
    df = spark.read.format("delta").load(f"{SILVER_PATH}/date={execution_date}")
    agg_df = df.groupBy("state", "brewery_type").count()

    agg_df.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("state") \
        .save(f"{GOLD_PATH}/breweries_summary/date={execution_date}")

    print(f"✅ Agregação concluída. Total de linhas: {agg_df.count()}")
    spark.stop()
    return True
