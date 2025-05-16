# src/extract.py
import requests
import pandas as pd
import io
from datetime import datetime
from src.s3_utils import upload_to_s3

API_URL = "https://api.openbrewerydb.org/v1/breweries"

def extract_breweries(execution_date: str) -> None:
    """
    Extrai os dados da API Open Brewery DB e armazena no bucket S3 (camada bronze).

    :param execution_date: Data de execução no formato YYYYMMDD
    :raises Exception: Se a requisição retornar código diferente de 200
    """
    print("🔹 Iniciando extração de dados da API Open Brewery DB")
    all_data = []
    page = 1
    per_page = 200

    while True:
        response = requests.get(API_URL, params={"page": page, "per_page": per_page})
        if response.status_code != 200:
            raise Exception(f"Erro na requisição: {response.status_code}")
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        print(f"✔️ Página {page} extraída com {len(data)} registros")
        page += 1

    df = pd.DataFrame(all_data)
    json_buffer = io.StringIO()
    df.to_json(json_buffer, orient="records", lines=True)
    timestamp = execution_date or datetime.today().strftime("%Y%m%d")

    upload_to_s3(
        bucket="bronze",
        key=f"breweries_raw_{timestamp}.json",
        body=json_buffer.getvalue()
    )

    print(f"✅ Extração concluída. Total de registros: {len(df)}")
