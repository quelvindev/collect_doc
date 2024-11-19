import pandas as pd 
import os
import re
from logger_config import LoggerConfig
from keys import Keys



class CollectAgenda:

    def __init__(self):
        self.logger = LoggerConfig().get_logger()
        self.spreadsheets = []
        self.key_agenda = Keys.get_key_agenda()
        self.dir_csv = Keys.get_dir_csv()
        self.dir_log = Keys.get_dir_log()

    
    def import_data(self):

        url = f'https://docs.google.com/spreadsheets/d/{self.key_agenda}/pubhtml'
        

        try:
            data = pd.read_html(url,encoding='latin1')
        except Exception as e:
            
            self.logger.info(f'Erro load spreadsheets agenda: {e}')
            print("Erro load spreadsheets agenda: ", e)
            data = []

        return data

    def split_data(self):
        data = self.import_data()
        tab0 = data[0] 
        tab1 = data[1]
        tab2 = data[2]
        tab3 = data[3]

        self.transform_data_tab1(tab0)

    


    def string_to_snake_case(self,string):
        string = re.sub(r"/"," ",string)
        string = re.sub(r" +","",string)
        string = re.sub(r" ","_",string)
        string = re.sub(r"([a-z])([A-Z])",r"\1_\2",string)
        return string.lower()

    def transform_data_tab1(self,df):
        
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

        # # PROMOVE NAME COLUMN
        df.columns = [self.string_to_snake_case(name) for name in column_names]

    
        self.export_data(df,'pepa.csv')




    
    def export_data(self,df,name):
        
        try:
            
            # Check if the file exists
            #file_exists = os.path.isfile(self.dir_csv)

        # Save the data to CSV in append mode
            df.to_csv(
                    name, 
                    index=False, 
                    sep=';', 
                    decimal='.', 
                   # mode='a', 
                    #header=not file_exists  # Write header only if the file does not exist
                )


            self.logger.info(f'sucessfull agenda') 
            print(f'sucessfull agenda') 
        except Exception as e:
            self.logger.info(f'Erro generate csv agenda: {e}')
            print(f'Erro generate csv agenda: {e}')
            

if __name__ == "__main__":
        
    agenda_collector = CollectAgenda()
    
    agenda_collector.split_data()
