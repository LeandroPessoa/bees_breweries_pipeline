# src/spark_utils.py
from pyspark.sql import SparkSession
import os

def create_spark_session(app_name: str) -> SparkSession:
    """
    Cria uma SparkSession configurada para uso com Delta Lake e MinIO (S3)

    :param app_name: Nome da aplicação Spark
    :return: SparkSession
    """
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("S3_ENDPOINT", "http://minio:9000")) \
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("S3_ACCESS_KEY", "admin")) \
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("S3_SECRET_KEY", "admin123")) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.jars.packages", \
                "org.apache.hadoop:hadoop-aws:3.3.2," \
                "com.amazonaws:aws-java-sdk-bundle:1.11.1026," \
                "io.delta:delta-core_2.12:2.3.0") \
        .config("spark.network.topology.enabled", "false") \
        .getOrCreate()
