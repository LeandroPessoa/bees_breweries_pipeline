#!/bin/bash

echo "⏳ Aguardando o LocalStack iniciar..."
awslocal s3 mb s3://bronze
awslocal s3 mb s3://silver
awslocal s3 mb s3://gold

echo "✅ Buckets criados com sucesso"

# (Opcional) recriar os parâmetros do SSM se necessário:
awslocal ssm put-parameter --name /datalake/bronze_path --type String --value s3a://bronze --overwrite
awslocal ssm put-parameter --name /datalake/silver_path --type String --value s3a://silver --overwrite
awslocal ssm put-parameter --name /datalake/gold_path --type String --value s3a://gold --overwrite

echo "✅ Parâmetros do SSM criados"