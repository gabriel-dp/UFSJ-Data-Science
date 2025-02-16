import pandas as pd
from unidecode import unidecode

UF_REVERSE = {
    'ACRE': 'AC',
    'ALAGOAS': 'AL',
    'AMAPA': 'AP',
    'AMAZONAS': 'AM',
    'BAHIA': 'BA',
    'CEARA': 'CE',
    'DISTRITO FEDERAL': 'DF',
    'ESPIRITO SANTO': 'ES',
    'GOIAS': 'GO',
    'MARANHAO': 'MA',
    'MATO GROSSO': 'MT',
    'MATO GROSSO DO SUL': 'MS',
    'MINAS GERAIS': 'MG',
    'PARA': 'PA',
    'PARAIBA': 'PB',
    'PARANA': 'PR',
    'PERNAMBUCO': 'PE',
    'PIAUI': 'PI',
    'RIO DE JANEIRO': 'RJ',
    'RIO GRANDE DO NORTE': 'RN',
    'RIO GRANDE DO SUL': 'RS',
    'RONDONIA': 'RO',
    'RORAIMA': 'RR',
    'SANTA CATARINA': 'SC',
    'SAO PAULO': 'SP',
    'SERGIPE': 'SE',
    'TOCANTINS': 'TO'
}

def get_files():
    FOLDER = "../data/infracoes"
    PREFIX = "infracoes_"
    SUFFIX = ""
    EXTENSION = "csv"
    
    files = []
    for y in range (2019, 2025):
        for m in range (1, 13):
            files.append(
                {
                    "year": y,
                    "month": m,
                    "path": f'{FOLDER}/{PREFIX}{y}_{m:02d}{SUFFIX}.{EXTENSION}'
                }
            )

    return files

def get_infractions_data():
    ENCODINGS = ['utf-8', 'utf-16']
    SEPARATORS = [',', ';']
    VARIATIONS = ['Codigo da Infracao', 'Codigo_Infracao', 'Cod _Infração', 'COD_INFRACAO']
    CORRECT = "INFRACAO"

    all_data = []

    for file in get_files():
        for encoding in ENCODINGS:
            for separator in SEPARATORS:
                try:
                    data = pd.read_csv(file["path"], sep=separator, encoding=encoding)
                    
                    if len(data.columns) == 1: # Wrong separator
                        continue

                    if len(data.columns) > 3: # Each state in a column
                        data = data.drop(0)
                        data.rename(columns={data.columns[0]: CORRECT})
                        data.columns = [CORRECT] + list(data.columns[1:])
                        data = data.melt(id_vars=[CORRECT], var_name="UF", value_name="Quantidade")

                    # Normalize columns
                    data.columns = [unidecode(col).upper() for col in data.columns]
                    for variation in VARIATIONS:
                        adjusted_variation = unidecode(variation).upper()
                        if adjusted_variation in data.columns:
                            data = data.rename(columns={adjusted_variation: CORRECT})
                            break
                    data = data[['UF', CORRECT, 'QUANTIDADE']]

                    # Adjust numbers
                    data['QUANTIDADE'] = data['QUANTIDADE'].fillna(0)
                    data['QUANTIDADE'] = data['QUANTIDADE'].astype(str).str.replace('.', '', regex=False).astype(int)

                    # Add time identifiers
                    data['MES'] = file['month']
                    data['ANO'] = file['year']                    
                    all_data.append(data)

                    break
                except UnicodeError: # Wrong encoding
                    continue

    # Concat all infractions
    df = pd.concat(all_data)
    df = df.groupby(['UF', 'ANO']).agg({'QUANTIDADE': 'sum'}).reset_index()
    df['UF'] = df['UF'].map(UF_REVERSE)
    df = df.rename(columns={'UF': 'state', 'ANO': 'year', 'QUANTIDADE' : 'quantity'}).sort_values(by=['year', 'state']) 

    return df