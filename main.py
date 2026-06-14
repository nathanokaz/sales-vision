from extract import pegar_dados_api
from transform import manipular_dados
from load import criar_base_de_dados
import schedule
import time

def main():
    print('[MAIN] Executando main')
    
    dados = pegar_dados_api()

    resultado = manipular_dados(dados)

    criar_base_de_dados(resultado)

    print('[MAIN] Pipeline executado com sucesso')

if __name__ == '__main__':
    main()

    schedule.every(30).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)