import requests
from utils.rate_limiter import rate_limiter

BASE_URL = "https://score.hsborges.dev"

def get_score(id_client, cpf):
    # Espera se necessário antes da requisição
    rate_limiter.wait_for_slot()

    url = f"{BASE_URL}/api/score?cpf={cpf}"
    headers = {
        "accept": "application/json",
        "client-id": id_client
    }

    response = requests.get(url, headers=headers)
    # Atualiza rate limiter com base na resposta
    rate_limiter.update_after_response(response)
    
    # Tratamento dos códigos de resposta
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        return response.json()
    elif response.status_code == 401:
        return {"error": "Client ID não informado ou inválido"}
    elif response.status_code == 429:
        return response.json()
    else:
        return {"error": f"Unexpected error, status code {response.status_code}"}
