import pandas as pd 
import os
import re
from logger_config import LoggerConfig
from keys import Keys



class CollectAgenda:

    def __init__(self):
        self.logger = LoggerConfig().get_logger()
        self.key_agenda = Keys.get_key_agenda()
        self.dir_log = Keys.get_arq_log()

    
    def import_data(self):

        url = f'https://docs.google.com/spreadsheets/d/{self.key_agenda}/pubhtml'

        try:
            data = pd.read_html(url,encoding='utf-8')
            self.logger.info(f'Sucess load agenda')
        except Exception as e:
            
            self.logger.info(f'Erro load spreadsheets agenda: {e}')
            print(f'Erro load spreadsheets agenda: {e}')
            data = []

        return data

    def string_to_snake_case(self,string):
        string = re.sub(r"/"," ",string)
        string = re.sub(r" +","",string)
        string = re.sub(r" ","_",string)
        string = re.sub(r"([a-z])([A-Z])",r"\1_\2",string)
        return string.lower()

    def transform_data(self):
        data = self.import_data()
        df = data[2]
        arq = Keys.get_arq_csv_agenda()

        # FRIST COLUMN DROP
        df = df.drop(df.columns[0], axis=1)

        # # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # # REMOVE LINE NULL
        df = df.dropna(how='all').reset_index(drop=True)
        

        df = df.iloc[3:].reset_index(drop=True)

        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

        # REPLACE QTD ; > /
        df[df.columns[5]] = df[df.columns[5]].str.replace("-", "")
    
        # #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "DATA"].reset_index(drop=True)
        df = df[df[df.columns[0]].str.strip().notna() & (df[df.columns[0]].str.strip() != "")].reset_index(drop=True)


        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,arq)

    
    def export_data(self,df,name):
        
        try:
            
            # Check if the file exists
            

        # Save the data to CSV in append mode
            df.to_csv(
                    name, 
                    index=False, 
                    sep=';', 
                    decimal='.'
                   
                    
                )


            self.logger.info(f'sucessfull agenda {name}') 
            print(f'sucessfull agenda {name}') 
        except Exception as e:
            self.logger.info(f'Erro generate csv agenda {name}: {e}')
            print(f'Erro generate csv agenda {name}: {e}')
        return
    
if __name__ == "__main__":
    collect = CollectAgenda()

    collect.transform_data()


        
