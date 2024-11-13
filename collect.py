import pandas as pd 


SPREADSHEETS = []
def import_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSx3uE5QRYjaQMmo3BvoY-5Ctd-OYQ7-nRh-eepLEw-w39AZUMLh5KwAeOvad34GrTN-2QiVEUT0RCg/pubhtml"

    try:
        data = pd.read_html(url)
    except Exception as e:
        print("Erro ao carregar a planilha:", e)

    return data

def collect_data():
    data = import_data()

    for i, table in enumerate(data):
        
        if i < len(SPREADSHEETS):
            SPREADSHEETS[i] = table  
        else:
            SPREADSHEETS.append(table) 
    
    df = SPREADSHEETS[0]

    return df 

def etl_data():
    df = collect_data()

    # FRIST COLUMN DROP
    df = df.drop(df.columns[0], axis=1)

    # linha = df[df[df.columns[0]].str.contains('data', case=False, na=False)].index[0]

    # FRIST COLUMN NAME
    # print(df.columns[0])

    # REMOVE NULL LINE
    df = df[df[df.columns[0]] != "F"]
    df = df.reset_index(drop=True)
    
    #PROMOVE NEMA COLUMN
    df.columns = df.iloc[0]  
    df = df.drop(0).reset_index(drop=True)  
    
    #REMOVE COLUMN NULL
    df = df.dropna(axis=1, how='all')

   
    print(df.columns)




       


if __name__ == "__main__":
    etl_data()