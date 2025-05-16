# src/config.py
import boto3
import os

def get_path_from_ssm(param_name: str, default_value: str = "") -> str:
    """
    Obtém valor de um parâmetro do SSM (via LocalStack) ou retorna valor padrão.

    :param param_name: Nome do parâmetro
    :param default_value: Valor padrão caso não encontrado
    :return: Valor obtido ou default
    """
    try:
        ssm = boto3.client(
            "ssm",
            endpoint_url=os.getenv("SSM_ENDPOINT", "http://localstack:4566"),
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        value = ssm.get_parameter(Name=param_name)["Parameter"]["Value"]
        print(f"✔️ {param_name} = {value}")
        return value
    except Exception as e:
        print(f"⚠️ Erro ao obter {param_name} do SSM: {e}")
        if default_value:
            print(f"➡️ Usando valor padrão: {default_value}")
            return default_value
        raise RuntimeError(f"Parâmetro {param_name} não encontrado e sem valor padrão definido.")


BRONZE_PATH = get_path_from_ssm("/datalake/bronze_path", "s3a://bronze")
SILVER_PATH = get_path_from_ssm("/datalake/silver_path", "s3a://silver")
GOLD_PATH = get_path_from_ssm("/datalake/gold_path", "s3a://gold")
