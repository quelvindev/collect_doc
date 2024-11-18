import pandas as pd 
import os
import logging
import re
from keys import key,DIR_CSV,DIR_LOG

logging.basicConfig(level=logging.INFO, filename=DIR_LOG, format="%(asctime)s - %(levelname)s - %(message)s")


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

def concat_data():

    spreadsheets = collect_data()
    df = pd.concat(spreadsheets,ignore_index=False)

    return df

def string_to_snake_case(string):
    string = re.sub("/"," ",string)
    string = re.sub(" +","",string)
    string = re.sub(" ","_",string)
    string = re.sub("([a-z])([A-Z])",r"\1_\2",string)
    return string.lower()

def transform_data():
    column_names = []

    df = concat_data()
    # FRIST COLUMN DROP
    df = df.drop(df.columns[0], axis=1)

    # REMOVE COLUMN NULL
    df = df.dropna(axis=1, how='all').reset_index(drop=True)

    # REMOVE LINE NULL
    df = df.dropna(how='all').reset_index(drop=True)
    
    df = df[df[df.columns[0]] != "CONTROLE DE RECEBIMENTO DIARIO (BONUS)"].reset_index(drop=True)

    df = df[df[df.columns[0]] != "f"].reset_index(drop=True)

    
    column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

   
    #REMOVE LINES DESCRITION
    df = df[df[df.columns[0]] != "Data"].reset_index(drop=True)

    # REPLACE DATE ; > /
    df[df.columns[0]] = df[df.columns[0]].str.replace(";", "/")

    # REPLACE HOUR ; > :
    df[df.columns[1]] = df[df.columns[1]].str.replace(";", ":")

    
    # PROMOVE NAME COLUMN
    df.columns = [string_to_snake_case(name) for name in column_names]

   
    return df   
def export_data():
    df = transform_data()
    try:

        remove_csv = os.path.dirname(DIR_CSV)
        remove_log = os.path.dirname(DIR_LOG)

        if not os.path.exists(remove_csv):
            os.makedirs(remove_csv)

        if not os.path.exists(remove_log):
            os.makedirs(remove_log)
        
        # Check if the file exists
        file_exists = os.path.isfile(DIR_CSV)

       # Save the data to CSV in append mode
        df.to_csv(
                DIR_CSV, 
                index=False, 
                sep=';', 
                decimal='.', 
                mode='a', 
                header=not file_exists  # Write header only if the file does not exist
            )


        logging.info(f'sucessfull')   
    except Exception as e:
        logging.error(f'Erro generate csv: {e}')
        


