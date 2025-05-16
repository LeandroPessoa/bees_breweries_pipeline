# src/validate.py
from datetime import datetime
from src.spark_utils import create_spark_session
from src.config import BRONZE_PATH, SILVER_PATH, GOLD_PATH
from src.s3_utils import list_s3_objects
from pyspark.sql import functions as F


def validate_bronze_data(execution_date: str) -> None:
    print("🔸 Verificando camada Bronze")
    filename = f"breweries_raw_{execution_date}.json"
    json_file = f"{BRONZE_PATH}/{filename}"
    bucket = BRONZE_PATH.replace("s3a://", "").split("/")[0]
    key = "/".join(json_file.replace("s3a://", "").split("/")[1:])

    if key not in list_s3_objects(bucket, key):
        raise Exception(f"❌ Arquivo {json_file} não encontrado na Bronze")

    spark = create_spark_session("ValidateBronze")
    df = spark.read.json(json_file)

    if df.rdd.isEmpty():
        raise Exception("❌ Dados vazios na camada Bronze")

    expected_columns = {"id", "name", "brewery_type", "state", "city"}
    if not expected_columns.issubset(set(df.columns)):
        raise Exception(f"❌ Colunas esperadas ausentes na Bronze: {expected_columns - set(df.columns)}")

    for col in expected_columns:
        n_nulls = df.filter(F.col(col).isNull()).count()
        if n_nulls > 0:
            print(f"⚠️ {n_nulls} valores nulos em '{col}' na Bronze")

    duplicate_ids = df.groupBy("id").count().filter("count > 1").count()
    if duplicate_ids > 0:
        raise Exception(f"❌ IDs duplicados encontrados na Bronze: {duplicate_ids}")

    print("✅ Bronze OK")
    spark.stop()

def validate_silver_data(execution_date: str) -> None:
    print("🔸 Verificando camada Silver")
    spark = create_spark_session("ValidateSilver")
    df = spark.read.format("delta").load(f"{SILVER_PATH}/date={execution_date}")

    if df.rdd.isEmpty():
        raise Exception("❌ Dados vazios na camada Silver")

    if df.filter("state IS NULL").count() > 0:
        raise Exception("❌ Coluna 'state' contém nulos na Silver")
    if df.filter("brewery_type IS NULL").count() > 0:
        raise Exception("❌ Coluna 'brewery_type' contém nulos na Silver")

    duplicate_ids = df.groupBy("id").count().filter("count > 1").count()
    if duplicate_ids > 0:
        raise Exception(f"❌ IDs duplicados encontrados na Silver: {duplicate_ids}")

    print("✅ Silver OK")
    spark.stop()

def validate_gold_data(execution_date: str) -> None:
    print("🔸 Verificando camada Gold")
    spark = create_spark_session("ValidateGold")
    df = spark.read.format("delta").load(f"{GOLD_PATH}/breweries_summary/date={execution_date}")

    if df.rdd.isEmpty():
        raise Exception("❌ Dados vazios na camada Gold")

    expected_cols = {"state", "brewery_type", "count"}
    if not expected_cols.issubset(set(df.columns)):
        raise Exception(f"❌ Colunas esperadas ausentes na Gold: {expected_cols - set(df.columns)}")

    if df.filter(F.col("count") <= 0).count() > 0:
        raise Exception("❌ Registros com 'count' menor ou igual a zero na Gold")

    duplicates = df.groupBy("state", "brewery_type").count().filter("count > 1").count()
    if duplicates > 0:
        raise Exception(f"❌ Duplicatas encontradas na Gold: {duplicates}")

    print("✅ Gold OK")
    spark.stop()