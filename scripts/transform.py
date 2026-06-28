import pandas 
from deep_translator import GoogleTranslator

def criar_data_frame(dados):
    return pandas.DataFrame(dados['products'])

def tratar_e_gerar_dados(data_frame):
    data_frame = data_frame.rename(columns={
        'title': 'nome',
        'description': 'descricao',
        'category': 'categoria',
        'price': 'preco',
        'rating': 'nota',
        'stock': 'estoque',
        'brand': 'marca'
        })
    
    data_frame = data_frame.drop(columns=[
        'tags', 'dimensions', 'reviews', 'meta', 'weight',
        'warrantyInformation', 'shippingInformation',
        'availabilityStatus', 'returnPolicy', 'minimumOrderQuantity',
        'sku', 'discountPercentage', 'images', 'thumbnail'
        ])
    
    data_frame['categoria'] = data_frame['categoria'].fillna('Desconhecida')
    data_frame['marca'] = data_frame['marca'].fillna('Sem marca')

    data_frame['valor_total_estoque'] = round(data_frame['estoque'] * data_frame['preco'], 2)

    data_frame['nivel_estoque'] = data_frame['estoque'].apply(lambda x: 'Alto risco' if x < 10
                                              else 'Médio risco' if x < 30
                                              else 'Baixo risco')
    
    data_frame['nivel_avaliacao'] = data_frame['nota'].apply(lambda x: 'Excelente' if x >= 4.5
                                             else 'Bom' if x >= 3
                                             else 'Ruim')
    
    media_preco = data_frame['preco'].mean()
    data_frame['preco_relativo'] = data_frame['preco'].apply(lambda x: 'Acima da média' if x > media_preco
                                             else 'Abaixo da média')
    
    score = (data_frame['nota'] * 2 + (data_frame['estoque'] / 10) - (data_frame['preco'] / 1000))
    data_frame['score_produto'] = round(((score - score.min()) / (score.max() - score.min())) * 100, 2)

    data_frame['status_score'] = data_frame['score_produto'].apply(lambda x: 'Excelente' if x >= 75
                                                   else 'Bom' if x >= 40
                                                   else 'Ruim')

    dicionario_categorias = {
        'beauty' : 'Beleza',
        'fragrances' : 'Fragrâncias',
        'groceries' : 'Compras',
        'furniture' : 'Móveis',
        'home-decoration' : 'Decoração casa',
        'kitchen-accessories' : 'Acessórios cozinha',
        'laptops' : 'Notebooks',
        'mens-shirts' : 'Camisetas masculinas',
        'mens-watches' : 'Relogios masculinos',
        'mobile-accessories' : 'Acessórios para celular',
        'motorcycle' : 'Motos',
        'skin-care' : 'Skin care',
        'smartphones' : 'Celulares',
        'sports-accessories' : 'Acessórios esportivos',
        'sunglasses' : 'Óculos de sol',
        'tablets' : 'Tablets',
        'tops' : 'Tops',
        'vehicle' : 'Veículos',
        'womens-bags' : 'Bolsas Femininas',
        'womens-dresses' : 'Vestidos Femininos',
        'womens-jewellery' : 'Jóias',
        'womens-shoes' : 'Tênis feminino',
        'womens-watches' : 'Relógios femininos',
        'mens-shoes' : 'Tênis masculino'
    }

    data_frame['categoria'] = data_frame['categoria'].map(dicionario_categorias)

    return data_frame

def criar_dim_produtos(data_frame):
    return data_frame[['id', 'nome', 'descricao']].drop_duplicates()

def criar_dim_categoria(data_frame):
    dim_categorias = data_frame[['categoria']].drop_duplicates().reset_index(drop=True)
    dim_categorias['categoria_id'] = dim_categorias.index + 1
    data_frame['categoria_id'] = data_frame['categoria'].map(dict(zip(dim_categorias['categoria'], dim_categorias['categoria_id'])))
    return dim_categorias

def criar_dim_marca(data_frame):
    dim_marcas = data_frame[['marca']].drop_duplicates().reset_index(drop=True)
    dim_marcas['marca_id'] = dim_marcas.index + 1
    data_frame['marca_id'] = data_frame['marca'].map(dict(zip(dim_marcas['marca'], dim_marcas['marca_id'])))
    return dim_marcas

def criar_listas(data_frame, dim_categorias, dim_marcas):
    lista_dim_produtos = list(zip(data_frame['id'].tolist(), data_frame['nome'].tolist(), data_frame['descricao'].tolist()))
    
    lista_dim_categorias = list(zip(dim_categorias['categoria_id'].tolist(), dim_categorias['categoria'].tolist()))
    
    lista_dim_marcas = list(zip(dim_marcas['marca_id'].tolist(), dim_marcas['marca'].tolist()))
    
    lista_produtos = list(zip(data_frame['id'].tolist(), data_frame['preco'].tolist(), data_frame['nota'].tolist(), data_frame['estoque'].tolist(),
                             data_frame['valor_total_estoque'].tolist(), data_frame['score_produto'].tolist(),
                             data_frame['nivel_estoque'].tolist(), data_frame['nivel_avaliacao'].tolist(),
                             data_frame['preco_relativo'].tolist(), data_frame['status_score'].tolist(),
                             data_frame['id'].tolist(), data_frame['categoria_id'].tolist(), data_frame['marca_id'].tolist()))
    
    return lista_dim_produtos, lista_dim_categorias, lista_dim_marcas, lista_produtos
    

def manipular_dados(dados):
    print('[TRANSFORM] Manipulando e tratando dados')

    # Faz a tradução porém removido devido ao tempo de execução do código
    #tradutor = GoogleTranslator(source='en', target='pt')
    #df['descricao'] = df['descricao'].apply(lambda x: tradutor.translate(x))
    #df['nome'] = df['nome'].apply(lambda x: tradutor.translate(x))
    
    data_frame = criar_data_frame(dados)
    data_frame_tratado = tratar_e_gerar_dados(data_frame)
    dim_produtos = criar_dim_produtos(data_frame_tratado)
    dim_categorias = criar_dim_categoria(data_frame_tratado)
    dim_marcas = criar_dim_marca(data_frame_tratado)
    lista_dim_produtos, lista_dim_categorias, lista_dim_marcas, lista_produtos = criar_listas(data_frame_tratado, dim_categorias, dim_marcas)

    return {'lista_dim_produtos' : lista_dim_produtos, 
            'lista_dim_categorias' : lista_dim_categorias, 
            'lista_dim_marcas' : lista_dim_marcas, 
            'lista_produtos' : lista_produtos,
            
            'data_frame_tratado' : data_frame_tratado,
            'dim_produtos' : dim_produtos,
            'dim_categorias' : dim_categorias,
            'dim_marcas' : dim_marcas}
    
    
