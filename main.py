# main.py
from collect_bonus import CollectBonus
from collect_preentrada import CollectPreEntrada

if __name__ == '__main__':
    
    collector = CollectBonus()
    preentrada_collector = CollectPreEntrada()
        
    collector.export_data()
    preentrada_collector.split_data()
