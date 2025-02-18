import os
import pandas as pd

def get_files():
    PATH = os.environ.get("PATH_DATA", "..")
    FOLDER = f"{PATH}/data/frota"
    PREFIX = "frota_"
    SUFFIX = ""
    EXTENSION = "xls"

    files = []
    for i in range (2004, 2025):
        files.append(
            {
                "year": i,
                "path": f'{FOLDER}/{PREFIX}{i}{SUFFIX}.{EXTENSION}'
            }
        )

    return files

def get_vehicles_data():
    all_data = []

    for file in get_files():    
        excel_file = pd.ExcelFile(file['path'])
        data = pd.read_excel(file['path'], sheet_name=excel_file.sheet_names[-1], skiprows=3, header=0)

        data.columns = (
            data.columns.str.normalize('NFKD')  # Decompose unicode characters
            .str.encode('ascii', errors='ignore')  # Remove non-ASCII characters
            .str.decode('utf-8')  # Decode back to UTF-8
            .str.strip()  # Remove leading/trailing spaces
            .str.lower()  # Convert to lowercase
        )

        data['ano'] = file['year']
        data['mes'] = file['year']

        all_data.append(data)

    # Concatenar as frotas
    df = pd.concat(all_data)
    # Agregar a frota por município
    df = df.sort_values('ano').groupby(['uf', 'ano']).agg({'total': 'sum'}).reset_index()
    df = df.rename(columns={'uf': 'state', 'total': 'quantity', 'ano': 'year'}).sort_values(by=['year', 'state']) 

    return df