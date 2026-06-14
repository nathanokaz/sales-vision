from extract import pegar_dados_api
from transform import manipular_dados
from load import criar_base_de_dados

def main():
    
    print('[MAIN] Executando main')
    dados = pegar_dados_api()
    df, dim_produto, dim_categoria, dim_marca, fato_produtos = manipular_dados(dados)
    criar_base_de_dados(df, dim_produto, dim_categoria, dim_marca, fato_produtos)

if __name__ == '__main__':
    main()