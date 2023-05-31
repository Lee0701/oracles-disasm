
import sys
import re
import yaml
import os.path
from PIL import Image, ImageDraw, ImageFont

columns = 16
glyph_width = 8
glyph_height = 16

image_height = 8192
image_width = glyph_width * 16

first_bank = int(sys.argv[4], 16)
offset = int(sys.argv[5], 16)

black = (0, 0, 0)
white = (255, 255, 255)

def get_filepath(filename):
    return os.path.dirname(filename)

def load_charset(charset_file):
    with open(charset_file, 'r', encoding='utf-8') as f:
        chars = f.read()

    chars = re.sub(r'[^\S\r\n]', '', chars)
    chars = re.sub(r'\\u([0-9a-fA-F]{1,6})', lambda x: chr(int(x.group(1), 16)), chars)
    chars = [line.ljust(16, chr(0)) for line in chars.split('\n')]
    return chars

def gen_bitmap(font_def, filepath):
    file_name = os.path.join(filepath, font_def['file_name'])
    charset_file = os.path.join(filepath, font_def['charset'])
    offset_x = font_def.get('offset_x', 0)
    offset_y = font_def.get('offset_y', 0)

    charset = load_charset(charset_file)

    width = columns * glyph_width
    height = len(charset) * glyph_height

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img, 'RGBA')

    draw.rectangle((0, 0, width, height), fill=black)

    src = Image.open(file_name)
    for j, line in enumerate(charset):
        for i, ch in enumerate(line):
            src_x  = i * glyph_width
            src_y  = j * glyph_height
            x = i * glyph_width + offset_x
            y = j * glyph_height + offset_y

            img.paste(src.crop((src_x, src_y, x+glyph_width, y+glyph_height)), (x, y))
    
    return img, charset

def gen_outline(font_def, filepath):
    font_name = os.path.join(filepath, font_def['font_name'])
    font_size = font_def['font_size']
    charset_file = os.path.join(filepath, font_def['charset'])
    offset_x = font_def.get('offset_x', 0)
    offset_y = font_def.get('offset_y', 0)

    charset = load_charset(charset_file)

    width = columns * glyph_width
    height = len(charset) * glyph_height

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img, 'RGBA')

    draw.rectangle((0, 0, width, height), fill=black)

    font_size = 12
    font = ImageFont.truetype(font_name, font_size)

    for j, line in enumerate(charset):
        for i, ch in enumerate(line):
            x = i * glyph_width + offset_x
            y = j * glyph_height + offset_y
            draw.text((x, y), ch, fill=white, font=font)
    
    return img, charset

def mark_table(table, charset, index=0):
    for j, line in enumerate(charset):
        for i, ch in enumerate(line):
            code = ord(ch)
            table[code] = index
            index += 1
    return index

def gen_table_file(table):
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

    output = '\n'.join(lines)
    return output


def main():
    fontset_deffile = sys.argv[1]
    filepath = get_filepath(fontset_deffile)
    with open(fontset_deffile, 'r') as f:
        fontset = yaml.safe_load(f)['fontset']

    table = [0 for _ in range(0x40000)]

    output_img = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(output_img, 'RGBA')
    draw.rectangle((0, 0, image_width, image_height), fill=black)

    index = 0
    offset_y = 0
    for font_def in fontset:
        font_type = font_def['type']
        if font_type == 'bitmap':
            font, charset = gen_bitmap(font_def, filepath)
            index += mark_table(table, charset, index)
            output_img.paste(font, (0, offset_y))
            offset_y += font.height
        elif font_type == 'outline':
            font, charset = gen_outline(font_def, filepath)
            index += mark_table(table, charset, index)
            output_img.paste(font, (0, offset_y))
            offset_y += font.height

    open(sys.argv[2], 'w').write(gen_table_file(table))
    output_img.save(sys.argv[3], 'png')

main()
