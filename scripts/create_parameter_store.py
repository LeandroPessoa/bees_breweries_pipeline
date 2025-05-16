import boto3

# Cliente do SSM conectado ao LocalStack
ssm = boto3.client(
    "ssm",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Dicionário com os parâmetros a serem criados
parameters = {
    "/datalake/bronze_path": "s3a://bronze",
    "/datalake/silver_path": "s3a://silver",
    "/datalake/gold_path": "s3a://gold"
}

# Criação dos parâmetros
for name, value in parameters.items():
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type="String",
        Overwrite=True
    )
    print(f"✅ Parâmetro criado: {name} = {value}")
