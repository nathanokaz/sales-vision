import requests

def pegar_dados_api():

    url = ('https://dummyjson.com/products?limit=0')
    response = requests.get(url)
    if response.status_code == 200: 
        print('[EXTRACT] API carregada com sucesso')
        return response.json()
    else:
        print('[EXTRACT] Erro ao consultar api')
        return None
