from pathlib import Path
import json

def meatloaf_date()-> str:
    anteatery=Path('.\\database\\anteatery_database.json').absolute()
    brandywine=Path('.\\database\\brandywine_database.json').absolute()
    a=open(anteatery)
    b=open(brandywine)
    a_data= json.load(a)
    b_data= json.load(b)
    a.close()
    b.close()
    a_keys=a_data.keys()
    b_keys = b_data.keys()

    for key in a_keys:
        Lunch= a_data[key]['Lunch']
        Dinner= a_data[key]['Dinner']
        for area in Lunch:
            for item in Lunch[area]:
                if not item.find('Meatloaf')==-1:
                    return key
        for area in Dinner:
            for item in Dinner[area]:
                if not item.find('meatloaf')==-1:
                    return key
    for key in b_keys:
        Lunch= b_data[key]['Lunch']
        Dinner= b_data[key]['Dinner']
        for area in Lunch:
            for item in Lunch[area]:
                if not item.find('Meatloaf')==-1:
                    return key
        for area in Dinner:
            for item in Dinner[area]:
                if not item.find('meatloaf')==-1:
                    return key
    return False
    

            
        

if __name__ =='__main__':
    response=meatloaf_date()
    p=Path('.\\database\\meatloaf_day.txt').absolute()
    opened_file=open(p,'w')
    opened_file.write(str(response))
    opened_file.close()
