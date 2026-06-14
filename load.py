import mysql.connector
import pandas

def cria_csvs(resultado):
    resultado[4].to_csv('csvs/fato_produtos.csv', sep=';', index=False)
    resultado[5].to_csv('csvs/dim_produtos.csv', sep=';', index=False)
    resultado[6].to_csv('csvs/dim_categorias.csv', sep=';', index=False)
    resultado[7].to_csv('csvs/dim_marcas.csv', sep=';', index=False)

def conectar_banco():
    conexao = mysql.connector.connect(host='localhost', database='teste', user='root', password='8676')

    if conexao.is_connected():
        print('[LOAD] Conectado ao banco de dados')
        cursor = conexao.cursor()

    return conexao, cursor

def criar_tables(banco_de_dados):
    banco_de_dados[1].execute('''CREATE TABLE IF NOT EXISTS dim_produtos (
                   produto_id INT PRIMARY KEY,
                   nome VARCHAR(100),
                   descricao TEXT)''')
    print('[LOAD] Criada table dim_produto')

    banco_de_dados[1].execute('''CREATE TABLE IF NOT EXISTS dim_categorias (
                   categoria_id INT PRIMARY KEY,
                   categoria VARCHAR(50))''')
    print('[LOAD] Criada table dim_categoria')

    banco_de_dados[1].execute('''CREATE TABLE IF NOT EXISTS dim_marcas (
                   marca_id INT PRIMARY KEY,
                   marca VARCHAR(50))''')
    print('[LOAD] Criada table dim_marcas')

    banco_de_dados[1].execute('''CREATE TABLE IF NOT EXISTS fato_produtos (
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   preco DECIMAL(10,2),
                   nota DECIMAL(4,2),
                   estoque INT,
                   valor_total_estoque DECIMAL(10,2),
                   score_produto DECIMAL(10,2),
                   nivel_estoque VARCHAR(50),
                   nivel_avaliacao VARCHAR(50),
                   preco_relativo VARCHAR(50),
                   status_score VARCHAR(50),

                   produto_id INT,
                   categoria_id INT,
                   marca_id INT,

                   FOREIGN KEY (produto_id) REFERENCES dim_produtos(produto_id),
                   FOREIGN KEY (categoria_id) REFERENCES dim_categorias(categoria_id),
                   FOREIGN KEY (marca_id) REFERENCES dim_marcas(marca_id))''')
    
    banco_de_dados[0].commit()
    print('[LOAD] Criada table fato_produtos')

def insert_dim_produtos(banco_de_dados, resultado):
    banco_de_dados[1].executemany('''INSERT IGNORE INTO dim_produtos (produto_id, nome, descricao)
                   VALUES (%s, %s, %s)''', resultado[0])
    banco_de_dados[0].commit()
    print('[LOAD] Insert realizado em: dim_produtos')

def insert_dim_categorias(banco_de_dados, resultado):
    banco_de_dados[1].executemany('''INSERT IGNORE INTO dim_categorias (categoria_id, categoria)
                       VALUES (%s, %s)''', resultado[1])
    banco_de_dados[0].commit()
    print('[LOAD] Insert realizado em: dim_categorias')

def insert_dim_marcas(banco_de_dados, resultado):
    banco_de_dados[1].executemany('''INSERT IGNORE INTO dim_marcas (marca_id, marca)
                       VALUES (%s, %s)''', resultado[2])
    banco_de_dados[0].commit()
    print('[LOAD] Insert realizado em: dim_marcas')

def insert_fato_produtos(banco_de_dados, resultado):
    banco_de_dados[1].executemany('''INSERT IGNORE INTO fato_produtos
                       (preco, nota, estoque, valor_total_estoque, score_produto,
                       nivel_estoque, nivel_avaliacao, preco_relativo, status_score,
                       produto_id, categoria_id, marca_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', resultado[3])
    banco_de_dados[0].commit()
    print('[LOAD] Insert realizado em: fato_produtos')

def criar_base_de_dados(resultado):
    cria_csvs(resultado)

    banco_de_dados = conectar_banco()

    criar_tables(banco_de_dados)

    insert_dim_produtos(banco_de_dados, resultado)
    insert_dim_categorias(banco_de_dados, resultado)
    insert_dim_marcas(banco_de_dados, resultado)
    insert_fato_produtos(banco_de_dados, resultado)

    banco_de_dados[1].close()
    banco_de_dados[0].close()