# src/s3_utils.py
import boto3
import os


def get_s3_client():
    """
    Retorna um cliente boto3 configurado para MinIO
    """
    return boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id=os.getenv("S3_ACCESS_KEY", "admin"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY", "admin123")
    )

def upload_to_s3(bucket: str, key: str, body: str) -> None:
    """
    Envia um conteúdo string para o bucket S3 informado

    :param bucket: nome do bucket
    :param key: caminho + nome do arquivo
    :param body: conteúdo em string
    """
    s3 = get_s3_client()
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    print(f"📤 Enviado para S3: s3://{bucket}/{key}")

def list_s3_objects(bucket: str, prefix: str) -> list:
    """
    Lista objetos em um bucket S3 dado um prefixo
    """
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj['Key'] for obj in response.get('Contents', [])]
