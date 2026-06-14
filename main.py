from extract import pegar_dados_api
from transform import manipular_dados
from load import criar_base_de_dados

def main():
    print('[MAIN] Executando main')
    
    dados = pegar_dados_api()

    resultado = manipular_dados(dados)

    criar_base_de_dados(resultado)

if __name__ == '__main__':
    main()