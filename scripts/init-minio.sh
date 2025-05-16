#!/bin/sh

# Aguarda o MinIO iniciar
sleep 5

# Cria os buckets bronze, silver e gold
mc alias set local http://localhost:9000 admin admin123
mc mb --ignore-existing local/bronze
mc mb --ignore-existing local/silver
mc mb --ignore-existing local/gold