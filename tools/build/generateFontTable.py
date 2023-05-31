
import sys
import re

# python3 generateFontTable.py [input.txt] [output.s] [bank] [offset]
# bank and offset are to be hex

with open(sys.argv[1], 'r', encoding='utf8') as f:
    chars = f.read()

first_bank = int(sys.argv[3], 16)
offset = int(sys.argv[4], 16)

chars = re.sub(r'\s', '', chars)
chars = re.sub(r'\\u([0-9a-fA-F]{1,5})', lambda x: chr(int(x.group(1))), chars)

table = [0 for i in range(0x40000)]
for (i, c) in enumerate(list(chars)):
    code = ord(c)
    index = i + offset
    table[code] = index

lines = []
lines.append('')
bank = first_bank
for (c, i) in enumerate(table):
    str = '%04x' % i
    a = str[0:2]
    b = str[2:4]
    if (c % (0x4000/2)) == 0:
        lines.append('.BANK $%x SLOT 1\n.ORG $0000' % (bank))
        bank += 1
        if c == 0:
            lines.append('gfx_font_unicode_table:')
    line = '\t.db $%s $%s' % (a, b)
    if i != 0 and c >= 0x20:
        line += ' ; U+%04x %s' % (c, chr(c))
    lines.append(line)

print([len(l) for l in lines])
output = '\n'.join(lines)

with open(sys.argv[2], 'w', encoding='utf8') as f:
    f.write(output)
