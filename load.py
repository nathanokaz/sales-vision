import mysql.connector

def criar_base_de_dados(df):
    df.to_csv('dados.csv', sep=';', index=False)
    
    conexao = mysql.connector.connect(host='localhost',
                                      database='sales_vision',
                                      user='root',
                                      password='8676')
    
    if conexao.is_connected():
        print('conectado ao banco de dados')
    
