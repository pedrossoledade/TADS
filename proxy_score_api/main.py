from api.score_api import get_score

id_client = "your_client_id_here"
#id_client = "000"
#id_client = ""
#cpfs = ["10054736099", "03930956144", "12345678900"]
cpfs = ["03930956144"]
#cpfs = [""]

for cpf in cpfs:
    print(get_score(id_client, cpf))
