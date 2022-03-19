
import sys
import yaml

with open(sys.argv[1], 'r', encoding='utf8') as f:
    content = yaml.safe_load(f)

for g in content['groups']:
    g['group'] = int(g['group'])
    for d in g['data']:
        if type(d['index']) != list:
            d['index'] = int(d['index'])
        else:
            for i, index in enumerate(d['index']):
                d['index'][i] = int(index)

def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))
yaml.add_representer(int, hexint_presenter)

with open(sys.argv[2], 'w', encoding='utf8') as f:
    yaml.dump(content, f, sort_keys=False, allow_unicode=True)
