import pandas as pd

def fix_price(price):
    price = price.replace(',', '.')
    if '€' in price:
        return float(price.replace('€', ''))
    elif 'lei' in price:
        return float(price.replace('lei', ''))/4.5
    elif 'Schimb' in price:
        return float('nan')
    raise Exception(price)
    
def fix_nr_anunt(nr):
    if type(nr) == list:
        return nr[0]
    elif type(nr) == str:
        return nr
    raise Exception("Weird anunt nr")
    
def fix_adaugat(adaugat):
    if len(adaugat):
        return adaugat[0]
    return ''

def read_housing(name):
    estates = pd.read_json(name, lines=True)
    estates["price"] = estates["price"].map(fix_price)
    estates["nr_anunt"] = estates["nr_anunt"].map(fix_nr_anunt)
    estates["adaugat_la"] = estates["adaugat_la"].map(fix_adaugat)
    
    estates.loc[(estates["type"] != "Case de vanzare Oradea") 
                & (estates["type"] != "Case de inchiriat Oradea") 
                & (estates["price"] > 4000), "type"] = "apartament_vanzare"
    estates.loc[(estates["type"] != "Case de vanzare Oradea") 
                & (estates["type"] != "Case de inchiriat Oradea") 
                & (estates["price"] <= 4000), "type"] = "apartament_inchiriat"
    estates.loc[~estates["type"]
                .isin({"Case de vanzare Oradea", "Case de inchiriat Oradea", 
                        "apartament_vanzare", "apartament_inchiriat"}), "type"] = "apartament_vanzare"
    return estates