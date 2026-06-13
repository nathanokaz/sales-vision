import mysql.connector

def criar_base_de_dados(df, dim_produto, dim_categoria, dim_marca, fato_produtos):
    df.to_csv('dados.csv', sep=';', index=False)
    
    conexao = mysql.connector.connect(host='localhost',
                                      database='sales_vision',
                                      user='root',
                                      password='8676')
    
    if conexao.is_connected():
        print('conectado ao banco de dados')
        cursor = conexao.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dim_produto (
                   produto_id INT PRIMARY KEY,
                   nome VARCHAR(100),
                   descricao TEXT)''')
    conexao.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dim_categoria (
                   categoria_id INT PRIMARY KEY AUTO_INCREMENT,
                   categoria VARCHAR(50))''')
    conexao.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dim_marca (
                   marca_id INT PRIMARY KEY AUTO_INCREMENT,
                   marca VARCHAR(50))''')
    conexao.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS fato_produtos (
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

                   FOREIGN KEY (produto_id) REFERENCES dim_produto(produto_id),
                   FOREIGN KEY (categoria_id) REFERENCES dim_categoria(categoria_id),
                   FOREIGN KEY (marca_id) REFERENCES dim_marca(marca_id))''')
    conexao.commit()

    cursor.executemany('''INSERT IGNORE INTO dim_produto (produto_id, nome, descricao)
                   VALUES (%s, %s, %s)''', dim_produto)
    conexao.commit()

    cursor.executemany('''INSERT IGNORE INTO dim_categoria (categoria)
                       VALUES (%s)''', dim_categoria)
    conexao.commit()

    cursor.executemany('''INSERT IGNORE INTO dim_marca (marca)
                       VALUES (%s)''', dim_marca)
    conexao.commit()

    cursor.executemany('''INSERT IGNORE INTO fato_produtos
                       (preco, nota, estoque, valor_total_estoque, score_produto,
                       nivel_estoque, nivel_avaliacao, preco_relativo, status_score,
                       produto_id, categoria_id, marca_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', fato_produtos)
    conexao.commit()

    cursor.close()
    conexao.close()