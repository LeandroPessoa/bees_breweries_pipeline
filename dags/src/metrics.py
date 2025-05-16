# src/metrics.py
from datetime import datetime
from src.spark_utils import create_spark_session
from src.config import GOLD_PATH


def log_metrics(execution_date: str) -> None:
    """
    Exibe a quantidade de registros da camada Gold no dia da execução.

    :param execution_date: Data no formato YYYYMMDD
    """
    print("🔹 Registrando métricas da camada Gold")
    spark = create_spark_session("LogMetrics")
    df = spark.read.format("delta").load(f"{GOLD_PATH}/breweries_summary/date={execution_date}")
    print(f"[METRIC] {datetime.today().isoformat()} - {df.count()} linhas agregadas")
    spark.stop()
