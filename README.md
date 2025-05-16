# 🍺 BEES – Desafio Técnico de Engenharia de Dados

## 📘 Visão Geral do Projeto

Este projeto foi desenvolvido como parte de um desafio técnico para a área de Engenharia de Dados na BEES. Seu objetivo é demonstrar a capacidade de construir uma pipeline de dados robusta, modular e escalável utilizando tecnologias amplamente adotadas no mercado.

A pipeline implementa um fluxo completo de dados que abrange:

- Extração de dados públicos a partir da **API Open Brewery DB**;
- Armazenamento dos dados brutos (camada **Bronze**) em um data lake simulado com o **MinIO**;
- Transformação e limpeza dos dados com **Apache Spark** e persistência como **tabelas Delta** (camada **Silver**);
- Agregações analíticas para criação de uma visão de negócio (camada **Gold**), também armazenada em formato Delta;
- Validações automáticas em cada etapa para garantir qualidade, formato e consistência dos dados.

Além disso, a solução é **totalmente containerizada** com **Docker Compose**, permitindo fácil execução local com componentes como Airflow, Spark, MinIO e LocalStack.

O projeto segue o padrão **Medallion Architecture** e foi desenvolvido com foco em:

- Clareza de código e modularização
- Observabilidade e reprocessamento por data
- Facilidade de testes unitários
- Expansibilidade futura para ferramentas de Data Quality (ex: Great Expectations) e de consulta (ex: Trino)

Este projeto implementa um pipeline de ingestão, transformação e agregação de dados da [Open Brewery DB](https://www.openbrewerydb.org/), utilizando **Apache Airflow**, **Spark com Delta Lake**, **MinIO** como data lake e **LocalStack** para simulação de serviços AWS (SSM). A arquitetura segue o padrão **Medallion** (Bronze, Silver, Gold).

---

## 🎯 Objetivos Atendidos

| Requisito                                             | Status |
|-------------------------------------------------------|--------|
| Consumo da API Open Brewery DB                        | ✅     |
| Orquestração com ferramenta (Airflow)                 | ✅     |
| Transformações com particionamento por localização    | ✅     |
| Arquitetura Medallion (Bronze, Silver, Gold)          | ✅     |
| Docker e Docker Compose                               | ✅     |
| Testes unitários                                      | ✅     |
| Validações automáticas após cada etapa                | ✅     |
| Modularização e qualidade de código                   | ✅     |
| Explicação técnica e execução documentada             | ✅     |

---

## 🧱 Arquitetura e Camadas

### 🔹 Bronze (Raw)
- Extração da API Open Brewery DB
- Salvamento de JSONs no MinIO: `s3://bronze/breweries_raw_<YYYYMMDD>.json`

### ⚪ Silver (Curated)
- Transformação com Spark (Delta Lake)
- Particionado por `state`
- Salvo em: `s3://silver/date=<YYYYMMDD>/`

### 🟡 Gold (Analytics)
- Agregação: contagem por `brewery_type` e `state`
- Salvo em: `s3://gold/breweries_summary/date=<YYYYMMDD>/`

---

## ⚙️ Execução local

### 1. Pré-requisitos
- Docker
- Docker Compose

### 2. Subir os containers

```bash
docker network create airflow-net
docker-compose build


docker-compose run --rm airflow-webserver airflow db init
docker-compose run --rm airflow-webserver airflow users create \
    --username admin --password admin \
    --firstname Admin --lastname User \
    --role Admin --email admin@example.com

docker-compose up -d

```

> Aguarde a criação da infraestrutura: Airflow, Redis, Postgres, MinIO, LocalStack.

### 3. Acessar interfaces

# Acesse o MinIO Console e valide se os buckets bronze, silver e gold estao presentes, caso nao esteja os crie com as configurações básicas.

# Acesse o Airflow e ative a dag.

| Serviço       | URL                         | Login  | Senha      |
|---------------|------------------------------|--------|------------|
| Airflow       | http://localhost:8080        | admin  | admin   |
| MinIO Console | http://localhost:9001        | admin  | admin123   |

---

## 🗂 Estrutura do Projeto

```bash
bees_breweries_pipeline/
├── dags/
│   ├── breweries_pipeline.py       # DAG principal
│   └── src/
│       ├── extract.py              # Extração da API
│       ├── transform.py            # Bronze ➝ Silver
│       ├── aggregate.py            # Silver ➝ Gold
│       ├── validate.py             # Validações por camada
│       ├── config.py               # SSM fake + paths
│       ├── s3_utils.py             # Operações com MinIO
│       └── spark_utils.py          # Sessão Spark
├── tests/                          # Testes unitários
├── scripts/                        # Inicialização do LocalStack
├── .env                            # Config do Airflow
├── docker-compose.yaml             # Infraestrutura
└── readme.md
```

---

## 🔄 DAG: `breweries_etl_pipeline`

Orquestrada com Airflow. Executa:

```text
extract_breweries
→ validate_bronze_data
→ transform_to_silver
→ validate_silver_data
→ aggregate_to_gold
→ validate_gold_data
→ log_metrics
```

- Agendamento: `@daily`
- Retry automático: 5 vezes
- Envio de e-mail em falhas (simulado via console)

---

## ✅ Validações de Qualidade

Implementadas como **steps independentes**:

| Camada   | Validações                                                                           |
|----------|---------------------------------------------------------------------------------------|
| Bronze   | Arquivo existe no S3, schema mínimo, colunas obrigatórias, ausência de duplicatas    |
| Silver   | Dados não nulos, colunas obrigatórias, IDs únicos                                    |
| Gold     | Campos esperados, `count > 0`, sem duplicatas por (`state`, `brewery_type`)          |

---

## 🧪 Executar Testes Unitários

Com o Airflow rodando:

```bash
docker-compose exec airflow-webserver pytest dags/tests/
```

---

## 💡 Decisões Técnicas e considerações

- **MinIO** foi utilizado para simular um data lake compatível com S3, permitindo testes locais.
- **Spark** foi escolhido pela escalabilidade e compatibilidade com Delta Lake.
- **LocalStack** permite simulação de SSM para carregar dinamicamente os paths dos buckets.
- Todas as etapas são **idempotentes** e podem ser reexecutadas com segurança por data.
- O uso de um motor de consulta sql como o Trino poderia ser usado para disponibilizar os dados em plataformas de BI/Data Visualization.
- O uso de Great Expectations, embora recomendável, não foi utilizado no projeto.

---

