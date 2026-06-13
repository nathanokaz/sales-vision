import requests

def pegar_dados_api():
    url = ('https://dummyjson.com/products?limit=0')
    response = requests.get(url)
    if response.status_code == 200: 
        return response.json()
    else:
        return 'erro ao consultar api'
