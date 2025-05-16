# src/transform.py
from datetime import datetime
from src.spark_utils import create_spark_session
from src.config import BRONZE_PATH, SILVER_PATH
from pyspark.sql import functions as F


def transform_to_silver(execution_date: str) -> bool:
    """
    Lê os dados da Bronze em JSON, filtra e salva como Delta particionado por estado (Silver).

    :param execution_date: Data de execução no formato YYYYMMDD
    :return: True se sucesso
    :raises: Exception se o arquivo JSON não for encontrado ou falhar a escrita
    """
    filename = f"breweries_raw_{execution_date}.json"
    json_file = f"{BRONZE_PATH}/{filename}"

    print("🔹 Iniciando transformação dos dados (Bronze ➝ Silver)")

    spark = create_spark_session("TransformSilver")
    df = spark.read.json(json_file)
    df = df.dropna(subset=["state"])
    df = df.select("id", "name", "brewery_type", "state", "city")

    df.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("state") \
        .save(f"{SILVER_PATH}/date={execution_date}")

    print("✅ Transformação concluída e dados salvos como Delta partitionado por estado")
    spark.stop()
    return True
