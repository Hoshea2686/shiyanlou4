# /urs/bin/python3
# -*-coding:utf-8-*-

import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--image', default='ascii_dora.png')
parser.add_argument('-o', '--output', type=str, default='output.txt')
args = parser.parse_args()
# print(args, args.image, args.output)
# Namespace(image='ascii_dora.png', output='output.txt') ascii_dora.png output.txt

img = args.image
output = args.output
width = 120
height = 60
charset = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def color2char(r, g, b, alpha):
	if alpha == 0:
		return ' '
	gray = 0.2126*r+0.7152*g+0.0722*b
	unit = len(charset)/256.0
	index = int(gray*unit)
	return charset[index]

if __name__ == '__main__':
	im = Image.open(img)
	im = im.resize((width, height), Image.NEAREST)
	txt = ''
	for i in range(height):
		for j in range(width):
			color = im.getpixel((j, i))
			txt += color2char(*color)
		txt += '\n'
	print(txt)
	with open(output, 'w') as f:
		f.write(txt) 