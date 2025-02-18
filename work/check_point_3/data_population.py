import os
import pandas as pd

PATH = os.environ.get("PATH_DATA", "..")
POPULATION_CSV_PATH = f"{PATH}/data/populacao/br_ibge_populacao_municipio.csv"

def get_population_data():
    df = pd.read_csv(POPULATION_CSV_PATH)
    df = df.rename(columns={'sigla_uf': 'UF'})
    df = df.groupby(['UF', 'ano']).agg({'populacao': 'sum'}).reset_index()
    df = df.rename(columns={'UF': 'state', 'ano': 'year', 'populacao': 'quantity'}).sort_values(by=['year', 'state']) 
    return df
