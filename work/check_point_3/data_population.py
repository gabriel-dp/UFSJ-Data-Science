import pandas as pd

POPULATION_CSV_PATH = '../data/populacao/br_ibge_populacao_municipio.csv'

def get_population_data():
    df = pd.read_csv(POPULATION_CSV_PATH)
    df = df.rename(columns={'sigla_uf': 'UF'})
    df = df.groupby(['UF', 'ano']).agg({'populacao': 'sum'}).reset_index()
    df = df.rename(columns={'UF': 'state', 'ano': 'year', 'populacao': 'quantity'}).sort_values(by=['year', 'state']) 
    return df
