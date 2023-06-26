#
# display.py
#

# copyright jay.nam@openstack.co.kr

import os
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path

import argparse

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

#print(f'ROOT={ROOT}')

PERSON_CLASS = 0
HEAD_CLASS = 1

def show_with_labels_in_original_format(opt):

	which = 'val' if opt.val else 'train'

	jason_path = f'{ROOT}/labels/{which}_original_format/{opt.path}.txt'

	with open(jason_path, 'r') as rf:
		x = rf.read()
		#print(x)

		aitem = json.loads(x)
			
		image_path = f'{ROOT}/images/{which}/{aitem["ID"]}.jpg'

		fig, ax = plt.subplots(1, 1)
		img = Image.open(image_path)

		ax.imshow(img)

		gtboxes = aitem["gtboxes"]

		rect = None

		for af in gtboxes:

			if opt.mask:
				# show only the "tag": "mask" persons.
				if af["tag"] != 'mask':
					continue
			else:
				# show only the "tag": "person" persons.
				if af["tag"] == 'mask':
					continue

			extra = af['extra']

			try:
				box_id = extra['box_id']

			except KeyError:
				continue

			#print(extra)

			if opt.ignore:
				# show only "extra": { "ignore": 1 ,,, } case.
				try:
					if extra["ignore"] != 1:
						continue

					print(f'box_id {box_id} extra.ignore is {extra["ignore"]}.')

				except KeyError:
					continue

			if opt.head_ignore:
				head_attr = af["head_attr"]

				try:
					if head_attr['ignore'] == 0:
						continue

					print(f'box_id {box_id} head_attr.ignore is {head_attr["ignore"]}.')

					hbox = af["hbox"]

					rect = patches.Rectangle(tuple(hbox[:2]), hbox[2], hbox[3],
							linewidth=1, edgecolor='r', facecolor='none')

				except KeyError:
					continue

			elif opt.head:

				head_attr = af["head_attr"]

				try:
					if head_attr['ignore'] == 1:
						continue

					hbox = af["hbox"]

					rect = patches.Rectangle(tuple(hbox[:2]), hbox[2], hbox[3],
							linewidth=1, edgecolor='r', facecolor='none')

				except KeyError:
					continue

				rect = patches.Rectangle(tuple(hbox[:2]), hbox[2], hbox[3],
						linewidth=1, edgecolor='r', facecolor='none')
			else:
				vbox = af["vbox"]

				rect = patches.Rectangle(tuple(vbox[:2]), vbox[2], vbox[3],
						linewidth=1, edgecolor='r', facecolor='none')

			ax.add_patch(rect)

			ax.text(rect.get_x(), rect.xy[1], box_id, color='red')

		plt.title(aitem['ID'])
		plt.show()

def show_with_labels_in_yolo_format(opt):

	which = 'val' if opt.val else 'train'

	jason_path = f'{ROOT}/labels/{which}/{opt.path}.txt'

	n  = 0;

	with open(jason_path, 'r') as rf:

		image_path = f'{ROOT}/images/{which}/{opt.path}.jpg'

		fig, ax = plt.subplots(1, 1)
		img = Image.open(image_path)

		ax.imshow(img)


		for x in rf:

			rect = None
			#print(f'{x}\n')

			a = x.split(' ')

			#print(f'a={a} {type(a)}')

			kind = int(a[0])

			#print(f'kind={type(kind)}')

			if opt.head:
				if kind == HEAD_CLASS:
					x = img.width * (float(a[1]) - float(a[3])/2)
					y = img.height * (float(a[2]) - float(a[4])/2)
					width = float(a[3]) * img.width
					height = float(a[4]) * img.height

					rect = patches.Rectangle((x, y), width, height,
							linewidth=1, edgecolor='r', facecolor='none')

			else:
				if kind == PERSON_CLASS:
					x = img.width * (float(a[1]) - float(a[3])/2)
					y = img.height * (float(a[2]) - float(a[4])/2)
					width = float(a[3]) * img.width
					height = float(a[4]) * img.height

					rect = patches.Rectangle((x, y), width, height,
							linewidth=1, edgecolor='r', facecolor='none')

			"""
			else:
				x = img.width * (float(a[1]) - float(a[3])/2)
				y = img.height * (float(a[2]) - float(a[4])/2)
				width = float(a[3]) * img.width
				height = float(a[4]) * img.height

				rect = patches.Rectangle((x, y), width, height,
							linewidth=1, edgecolor='r', facecolor='none')
			"""

			if rect:
				ax.add_patch(rect)

				ax.text(rect.get_x(), rect.xy[1], n, color='red')

				n += 1

		img.close()

		plt.title(opt.path)
		plt.show()

def show(opt):
	print(opt)

	if opt.original_format:
		show_with_labels_in_original_format(opt)
	else:
		show_with_labels_in_yolo_format(opt)

def usage():
	print(f'usage: python {__file__} filename')

#
# the default is to show vbox.
#
def parse_opt(known=False):
	parser = argparse.ArgumentParser()

	parser.add_argument('--ignore', action='store_true', help='show only "extra.ignore: 1" persons.')
	parser.add_argument('--head_ignore', action='store_true', help='show only "head_attr.ignore: 1" heads.')
	parser.add_argument('--mask', action='store_true', help='show only mask pictures.')
	parser.add_argument('--head', action='store_true', help='show only head.')
	parser.add_argument('--original_format', action='store_true', help='label in the original Jason format.')
	parser.add_argument('--val', action='store_true', help='validation')
	parser.add_argument('path')

	return parser.parse_known_args()[0] if known else parser.parse_args()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()
	else:
		opt = parse_opt()
		show(opt)
