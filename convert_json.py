import pandas as pd
import re
import json
import cmd, sys

input = input("Provide relative filepath to the JSON file:")
#input = r'C:\Users\a.bousquet\OneDrive - GlobalTranz\Documentation\American Freight Integration\EDW.POUPLOAD_GTZ-2020-10-15-1648.json'

input = input.replace("\\",r"\\")

print(input)

with open(input, 'r') as file:
    j = file.read()
    

start = re.compile(r'\\')
end = re.compile(r'.json')

filename_start_pos = start.finditer(input)
filename_end_pos = end.search(input).span(0)[0]


for pos in filename_start_pos:
    # get the last ending position of \\
    filename_start_pos = pos.end()

bad_node_end = re.compile('}\n(?={)')
last_node_end = re.compile('}\n(?!{)')

# print(j)

json_start = re.search('[{\\[]',j)

if json_start:
    start_pos = json_start.span(0)[0]
    j = j[start_pos:]

    if(json_start[0] == '{'):
        nodes = bad_node_end.sub('},\n',j)
        nodes = last_node_end.sub('}',nodes)
        j = '[' + nodes + ']'
    
    filename = input[filename_start_pos:filename_end_pos]

    print(filename)

    json_parsed = json.loads(j)
    # records = json_parsed
    df = pd.json_normalize(json_parsed)
    df.to_excel(f'./excel/{filename}.xlsx', sheet_name=filename[:10], index=False)
    df.to_csv(f'./csv/{filename}.csv', index=False)
    df.to_parquet(f'./parquet/{filename}.parquet', index=False)
else:
    print("Valid JSON not found")
