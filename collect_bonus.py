import pandas as pd 
import os
import re
from logger_config import LoggerConfig
from keys import Keys



class CollectBonus:

    def __init__(self):
        self.logger = LoggerConfig().get_logger()
        self.spreadsheets = []
        self.key_bonus = Keys.get_key_bonus()
        self.dir_csv = Keys.get_arq_csv_bonus()
        self.dir_log = Keys.get_arq_log()

    
    def import_data(self):

        url = f'https://docs.google.com/spreadsheets/d/{self.key_bonus}/pubhtml'

        try:
            data = pd.read_html(url,encoding='latin1')
        except Exception as e:
            
            self.logger.info(f'Erro load spreadsheets bonus: {e}')
            print(f'Erro load spreadsheets bonus: {e}')
            data = []

        return data

    def collect_data(self):
        data = self.import_data()

        for _, table in enumerate(data):

            self.spreadsheets.append(table)
                
        return self.spreadsheets 

    def concat_data(self):

        spreadsheets = self.collect_data()
        df = pd.concat(spreadsheets,ignore_index=False)

        return df

    def string_to_snake_case(self,string):
        string = re.sub(r"/"," ",string)
        string = re.sub(r" +","",string)
        string = re.sub(r" ","_",string)
        string = re.sub(r"([a-z])([A-Z])",r"\1_\2",string)
        return string.lower()

    def transform_data(self):

        df = self.concat_data()
        # FRIST COLUMN DROP
        df = df.drop(df.columns[[0,8,14,15]], axis=1)

        # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # REMOVE LINE NULL
        #df = df.dropna(how='all').reset_index(drop=True)

        
        

        
        #df = df[df[df.columns[0]] != "CONTROLE DE RECEBIMENTO DIARIO (BONUS)"].reset_index(drop=True)
        df = df[~df.apply(lambda row: row.map(lambda x: isinstance(x, str) and x.startswith("CONTROLE"))).any(axis=1)].reset_index(drop=True)



        df = df[df[df.columns[0]] != "f"].reset_index(drop=True)

        
        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

    
        #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "DATA"].reset_index(drop=True)

        # REPLACE DATE ; > /
        df[df.columns[0]] = df[df.columns[0]].str.replace(";", "/")

        # REPLACE HOUR ; > :
        df[df.columns[1]] = df[df.columns[1]].str.replace(";", ":")

        
        # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        return df   
    def export_data(self):
        df = self.transform_data()
        try:
            
            # Check if the file exists
            file_exists = os.path.isfile(self.dir_csv)

        # Save the data to CSV in append mode
            df.to_csv(
                    self.dir_csv, 
                    index=False, 
                    sep=';', 
                    decimal='.', 
                    mode='a', 
                    header=not file_exists  # Write header only if the file does not exist
                )


            self.logger.info(f'sucessfull bonus')   
        except Exception as e:
            self.logger.info(f'Erro generate csv bonus: {e}')
            


