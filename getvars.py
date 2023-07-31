import pandas as pd
import json

df=pd.read_excel('метки.xlsx')[2:]
VARIABLES=["client_name", "store_name_1", "store_name_2", "date", "product_name"]
client_name=['Иван','Александр']
store_name_1=['Эльдорадо','Мвидео']
store_name_2=['Эльдорадо','Мвидео']
date=['01.01.2011', '20.02.2022']
product_name=['утюг','сплит система Hi']

def filter_rows(row):
    return row['name'] not in VARIABLES

def create_hierarchy(row):
    start_var, end_var, name_var=row['start, ms'],row['end, ms'],row['name']
    data=[]


    hierarchy_list=[]
    filtered_df=df[(df['start, ms']>=start_var)&(df['end, ms']<=end_var)&(df['name']!=name_var)]
    for _, other_row in filtered_df.iterrows():
        if(other_row['name'] in VARIABLES):
            if(VARIABLES.index(other_row['name'])==0): data=client_name
            elif(VARIABLES.index(other_row['name'])==1): data=store_name_1
            elif(VARIABLES.index(other_row['name'])==2): data=store_name_2
            elif(VARIABLES.index(other_row['name'])==3): data=date
            else: data=product_name
        hierarchy_list.append((other_row['name'], *data, round((other_row['start, ms']-start_var)*1000), round((other_row['end, ms']-start_var)*1000)))

    output=json.dumps(hierarchy_list, ensure_ascii=False).replace('[', '(').replace(']', ')').replace('\"', "'")
    output=list(output)
    output[0]='['
    output[-1]=']'
    output=''.join(output)
    return output


def get_mark_json(data):
    output=data

    output['hierarchy']=output.apply(create_hierarchy, axis=1)
    output=output[output.apply(filter_rows, axis=1)]

    print(output)

    data_dict={}
    for name in output['name'].unique():
        rows=df[df['name']==name]
        nested_labels=rows['hierarchy'].tolist()
        data_dict[name]={'variables': nested_labels, 'template': rows['template'].tolist()}

    with open('marks.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, ensure_ascii=False)

        
get_mark_json(df)
