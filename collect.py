import pandas as pd 
import os
import logging
from keys import key

logging.basicConfig(level=logging.INFO, filename="programa.log", format="%(asctime)s - %(levelname)s - %(message)s")
SPREADSHEETS = []
def import_data():
    url = f'https://docs.google.com/spreadsheets/d/{key}/pubhtml'

    try:
        data = pd.read_html(url,encoding='latin1')
    except Exception as e:
        logging.error(f'Erro load spreadsheets: {e}')
        print("Erro load spreadsheets: ", e)
        

    return data

def collect_data():
    data = import_data()

    for i, table in enumerate(data):

        SPREADSHEETS.append(table)
            
    return SPREADSHEETS 

def join_data():

    spreadsheets = collect_data()
    df = pd.concat(spreadsheets,ignore_index=False)

    return df

def etl2_data():

    df = join_data()
    # FRIST COLUMN DROP
    if df.shape[1] > 0:
            df = df.drop(df.columns[0], axis=1)
    
    df = df[df[df.columns[0]] != "CONTROLE DE RECEBIMENTO DIARIO (BONUS)"].reset_index(drop=True)
    
    # PROMOVE NAME COLUMN
    df.columns = df.iloc[0]

    df = df[df[df.columns[0]] != "Data"].reset_index(drop=True)

    # REMOVE COLUMN NULL
    df = df.dropna(axis=1, how='all')

    # REMOVE LINE NULL
    df = df.dropna(how='all')


    # REPLACE ; > :
    df[df.columns[1]] = df[df.columns[1]].str.replace(";", ":")

   
    return df   
def export_data():
    df = etl2_data()
    try:
        # Check if the file exists
        file_exists = os.path.isfile('controle_bonus.csv')
        
        # Save the data to CSV in append mode
        df.to_csv(
            'controle_bonus.csv', 
            index=False, 
            sep=';', 
            decimal='.', 
            mode='a', 
            header=not file_exists  # Write header only if the file does not exist
        )
        logging.info(f'sucessfull')   
    except Exception as e:
        logging.error(f'Erro generate csv: {e}')
        print(f'Erro generate csv: {e}')


