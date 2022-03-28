
import sys
import csv
import yaml

with open(sys.argv[1], 'r', encoding='utf8') as f:
    base_content = yaml.safe_load(f)

patch_content = {}
with open(sys.argv[2], 'r', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        patch_content[row[0]] = row[1]

for g in base_content['groups']:
    for d in g['data']:
        if type(d['name']) == list:
            name = d['name'][0]
        elif type(d['name']) == str:
            name = d['name']
        else:
            name = None
        if name != None:
            if name in patch_content and patch_content[name] != '':
                d['text'] = patch_content[name]

def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))
yaml.add_representer(int, hexint_presenter)

with open(sys.argv[3], 'w', encoding='utf8') as f:
    yaml.dump(base_content, f, sort_keys=False, allow_unicode=True)
