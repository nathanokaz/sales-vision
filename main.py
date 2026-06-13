from extract import pegar_dados_api
from transform import manipular_dados
from load import criar_base_de_dados

def main():
    print('executando main')
    dados = pegar_dados_api()
    df = manipular_dados(dados)
    criar_base_de_dados(df)

if __name__ == '__main__':
    main()