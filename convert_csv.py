import pandas as pd
import re
import json
import cmd, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p','--path', help='provide the path to the Parquet file')
args = parser.parse_args()


if not args.path:
    input = input("Provide relative filepath to the Parquet file:")
else:
    input = args.path
#input = r'C:\Users\a.bousquet\OneDrive - GlobalTranz\Documentation\American Freight Integration\EDW.POUPLOAD_GTZ-2020-10-15-1648.json'

input = input.replace("\\",r"\\")
input = input.replace('"',r'')

print(input)

start = re.compile(r'\\')
end = re.compile(r'.csv')

filename_start_pos = start.finditer(input)
filename_end_pos = end.search(input).span(0)[0]

for pos in filename_start_pos:
    # get the last ending position of \\
    filename_start_pos = pos.end()
# print(j)

filename = input[filename_start_pos:filename_end_pos]

print(filename)

df = pd.read_csv(input)

# excel = df.to_excel(f'./excel/{filename}.xlsx', sheet_name=filename[:10], index=False)
json = df.to_json(f'./json/{filename}.json')
csv = df.to_parquet(f'./parquet/{filename}.parquet')

