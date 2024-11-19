import pandas as pd 
import os
import re
from logger_config import LoggerConfig
from keys import Keys



class CollectPreEntrada:

    def __init__(self):
        self.logger = LoggerConfig().get_logger()
        self.key_preentrada = Keys.get_key_preentrada()
        self.dir_log = Keys.get_arq_log()

    
    def import_data(self):

        url = f'https://docs.google.com/spreadsheets/d/{self.key_preentrada}/pubhtml'

        try:
            data = pd.read_html(url,encoding='utf-8')
            self.logger.info(f'Sucess load pre entrada')
        except Exception as e:
            
            self.logger.info(f'Erro load spreadsheets pre entrada: {e}')
            print(f'Erro load spreadsheets pre entrada: {e} ')
            data = []

        return data

    def split_data(self):
        data = self.import_data()
        tab0 = data[0] 
        tab1 = data[1]
        tab2 = data[2]
        tab3 = data[3]

        self.transform_data_tab0(tab0)
        self.transform_data_tab1(tab1)
        self.transform_data_tab2(tab2)
        self.transform_data_tab3(tab3)

    


    def string_to_snake_case(self,string):
        string = re.sub(r"/"," ",string)
        string = re.sub(r" +","",string)
        string = re.sub(r" ","_",string)
        string = re.sub(r"([a-z])([A-Z])",r"\1_\2",string)
        return string.lower()

    def transform_data_tab0(self,df):
        arq = Keys.get_arq_csv_tab0()
        # FRIST COLUMN DROP
        df = df.drop(df.columns[0], axis=1)

        # # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # # REMOVE LINE NULL
        df = df.dropna(how='all').reset_index(drop=True)
        

        df = df.iloc[1:].reset_index(drop=True)

        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

    
        # #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "MÊS"].reset_index(drop=True)
        df = df[df[df.columns[0]].str.strip().notna() & (df[df.columns[0]].str.strip() != "")].reset_index(drop=True)


        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,arq)

    def transform_data_tab1(self,df):

        arq = Keys.get_arq_csv_tab1()
        # FRIST COLUMN DROP
        df = df.drop(df.columns[0], axis=1)

        # # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # # REMOVE LINE NULL
        df = df.dropna(how='all').reset_index(drop=True)
        

        df = df.iloc[1:].reset_index(drop=True)

        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

    
        # #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "MÊS"].reset_index(drop=True)
        df = df[df[df.columns[0]].str.strip().notna() & (df[df.columns[0]].str.strip() != "")].reset_index(drop=True)


        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,arq)

    def transform_data_tab2(self,df):
        arq = Keys.get_arq_csv_tab2()
        # FRIST COLUMN DROP
        df = df.drop(df.columns[0], axis=1)

        # # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # # REMOVE LINE NULL
        df = df.dropna(how='all').reset_index(drop=True)
        

        df = df.iloc[1:].reset_index(drop=True)

        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

    
        # #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "DATA REC."].reset_index(drop=True)
        df = df[df[df.columns[0]].str.strip().notna() & (df[df.columns[0]].str.strip() != "")].reset_index(drop=True)


        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,arq)

    def transform_data_tab3(self,df):
        arq = Keys.get_arq_csv_tab3()
        # FRIST COLUMN DROP
        df = df.drop(df.columns[0], axis=1)

        # # REMOVE COLUMN NULL
        df = df.dropna(axis=1, how='all').reset_index(drop=True)

        # # REMOVE LINE NULL
        df = df.dropna(how='all').reset_index(drop=True)
        

        df = df.iloc[1:].reset_index(drop=True)

        column_names =   df.iloc[0].apply(lambda x: str(x) if pd.notnull(x) else "").tolist()

    
        # #REMOVE LINES DESCRITION
        df = df[df[df.columns[0]].str.upper() != "DATA REC."].reset_index(drop=True)
        df = df[df[df.columns[0]].str.strip().notna() & (df[df.columns[0]].str.strip() != "")].reset_index(drop=True)


        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,arq)
    
    def export_data(self,df,name):
        
        try:
            
            # Check if the file exists
            file_exists = os.path.isfile(name)

        # Save the data to CSV in append mode
            df.to_csv(
                    name, 
                    index=False, 
                    sep=';', 
                    decimal='.', 
                    mode='a', 
                    header=not file_exists  # Write header only if the file does not exist
                )


            self.logger.info(f'sucessfull pre entrada {name}') 
            print(f'sucessfull pre entrada {name}') 
        except Exception as e:
            self.logger.info(f'Erro generate csv pre entrada {name}: {e}')
            print(f'Erro generate csv pre entrada {name}: {e}')
        return


        
