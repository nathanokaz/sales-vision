import pandas 

def manipular_dados(dados):
    df = pandas.DataFrame(dados['products'])
    
    df = df.rename(columns={'title': 'nome',
                        'description': 'descricao',
                        'category': 'categoria',
                        'price': 'preco',
                        'rating': 'nota',
                        'stock': 'estoque',
                        'brand': 'marca',
                        'thumbnail': 'imagem'})
    
    df = df.drop(columns=['tags', 'dimensions', 'reviews', 'meta', 'weight',
                          'warrantyInformation', 'shippingInformation',
                          'availabilityStatus', 'returnPolicy', 'minimumOrderQuantity',
                          'sku', 'discountPercentage', 'images'
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

    return df
    
    
