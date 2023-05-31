
import sys
import re
from PIL import Image, ImageDraw, ImageFont

charset = sys.argv[1]
fontfile = sys.argv[2]
output = sys.argv[3]

glyph_width = 8
glyph_height = 16
x_offset = 0
y_offset = 5
image_height = 1024

with open(charset, 'r', encoding='utf-8') as f:
    chars = f.read()

chars = re.sub(r'[^\S\r\n]', '', chars)
chars = re.sub(r'\\u([0-9a-fA-F]{1,5})', lambda x: chr(int(x.group(1))), chars)
chars = chars.split('\n')

width = 16 * glyph_width
height = len(chars) * glyph_height

img = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(img, 'RGBA')

black = (0, 0, 0)
white = (255, 255, 255)

draw.rectangle((0, 0, width, height), fill=black)

font_size = 12
font = ImageFont.truetype(fontfile, font_size)

for j, line in enumerate(chars):
    for i, ch in enumerate(line):
        x = i * glyph_width + x_offset
        y = j * glyph_height + y_offset
        draw.text((x, y), ch, fill=white, font=font)

output_height = height // image_height
if height % image_height != 0:
    output_height = ((height // image_height) + 1) * image_height
output_img = Image.new("RGB", (width, output_height))
draw = ImageDraw.Draw(output_img, 'RGBA')
draw.rectangle((0, 0, width, height), fill=black)
output_img.paste(img, (0, 0))

output_img.save(output)