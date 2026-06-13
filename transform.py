import pandas 

def manipular_dados(dados):
    df = pandas.DataFrame(dados['products'])
    
    df = df.rename(columns={'title': 'nome',
                        'description': 'descricao',
                        'category': 'categoria',
                        'price': 'preco',
                        'rating': 'nota',
                        'stock': 'estoque',
                        'brand': 'marca',})
    
    df = df.drop(columns=['tags', 'dimensions', 'reviews', 'meta', 'weight',
                          'warrantyInformation', 'shippingInformation',
                          'availabilityStatus', 'returnPolicy', 'minimumOrderQuantity',
                          'sku', 'discountPercentage', 'images', 'thumbnail'
                          ])
    
    df['valor_total_estoque'] = df['estoque'] * df['preco']

    df['nivel_estoque'] = df['estoque'].apply(lambda x: 'Alto risco' if x < 10
                                              else 'Médio risco' if x < 30
                                              else 'Baixo risco')
    
    df['nivel_avaliacao'] = df['nota'].apply(lambda x: 'Excelente' if x >= 4.5
                                             else 'Bom' if x >= 3
                                             else 'Ruim')
    
    media_preco = df['preco'].mean()
    df['preco_relativo'] = df['preco'].apply(lambda x: 'Acima da média' if x > media_preco
                                             else 'Abaixo da média')
    
    score = (
        df['nota'] * 2 +
        (df['estoque'] / 10) -
        (df['preco'] / 1000)
    )
    df['score_produto'] = (
        (score - score.min()) /
        (score.max() - score.min())
    ) * 100

    df['status_score'] = df['score_produto'].apply(lambda x: 'Excelente' if x >= 75
                                                   else 'Bom' if x >= 40
                                                   else 'Ruim')
    
    df['categoria_id'] = df['categoria'].index + 1
    df['marca_id'] = df['marca'].index + 1
    
    dim_produto = list(zip(df['id'].tolist(), df['nome'].tolist(), df['descricao'].tolist()))
    dim_categoria = list(zip(df['categoria'].tolist()))
    dim_marca = list(zip(df['marca'].tolist()))
    fato_produtos = list(zip(df['preco'].tolist(), df['nota'].tolist(), df['estoque'].tolist(),
                             df['valor_total_estoque'].tolist(), df['score_produto'].tolist(),
                             df['nivel_estoque'].tolist(), df['nivel_avaliacao'].tolist(),
                             df['preco_relativo'].tolist(), df['status_score'].tolist(),
                             df['id'].tolist(), df['categoria_id'].tolist(), df['marca_id'].tolist()))

    return df, dim_produto, dim_categoria, dim_marca, fato_produtos
    
    
