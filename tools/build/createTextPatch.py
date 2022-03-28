
import sys
import csv
import yaml

with open(sys.argv[1], 'r', encoding='utf8') as f:
    base_content = yaml.safe_load(f)

patch_content = {}

for g in base_content['groups']:
    for d in g['data']:
        if type(d['name']) == list:
            for name in d['name']:
                patch_content[name] = d['text']
        elif type(d['name']) == str:
            name = d['name']
            patch_content[name] = d['text']

def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))
yaml.add_representer(int, hexint_presenter)

with open(sys.argv[2], 'w', encoding='utf8') as f:
    writer = csv.writer(f, delimiter='\t')
    for row in patch_content.items():
        writer.writerow(row)
