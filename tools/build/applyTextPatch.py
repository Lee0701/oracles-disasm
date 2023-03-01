
import os
import sys
import yaml

with open(sys.argv[1], 'r', encoding='utf8') as f:
    base_content = yaml.safe_load(f)

with open(sys.argv[2], 'r', encoding='utf8') as f:
    patch_content = yaml.safe_load(f)

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

os.makedirs(os.path.dirname(sys.argv[3]), exist_ok=True)
with open(sys.argv[3], 'w', encoding='utf8') as f:
    yaml.dump(base_content, f, sort_keys=False, allow_unicode=True)
