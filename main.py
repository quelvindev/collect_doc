# main.py
from collect_bonus import CollectBonus
from collect_preentrada import CollectPreEntrada
from collect_agenda import CollectAgenda

if __name__ == '__main__':
    
    collector = CollectBonus()
    preentrada_collector = CollectPreEntrada()
    agenda_coolector = CollectAgenda()
        
    collector.export_data()
    #preentrada_collector.split_data()
    #agenda_coolector.transform_data()
