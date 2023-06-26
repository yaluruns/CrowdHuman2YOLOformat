"""
integrity_check.py
"""

import sys
import json

def convert(argv):

	with open(argv[0], 'r') as rf:
		n = 0
			
		for x in rf:
			pic = json.loads(x)

			print(f'[{n}] {pic["ID"]} checking ....')

			for item in pic['gtboxes']:
				#
				# "tag": "mask" means "extra": {"ignore": 1}.
				#
				if item['tag'] == 'mask':
					extra = item['extra']
					if extra['ignore'] != 1:
						print(f'\ttag is mask but extra.ignore is {extra["ignore"]}.\n')
				else:
					extra = item['extra']
					box_id = extra["box_id"]

					try:
						ignore = extra['ignore']
						if ignore == 1:
							print(f'\t[{box_id}] \'tag\' is not \'mask\' but extra.ignore is {ignore}.')

					except KeyError:
						pass

					head_attr = item['head_attr']

					if head_attr:
						#extra = item['extra']
						#box_id = extra["box_id"]

						ignore = head_attr["ignore"]
						unsure = head_attr['unsure']

						#
						# "head_attr": "ignore": 1 case
						# there is no head in this person.
						#
						if ignore == 1:
							print(f'\t[{box_id}] \'tag\' is not \'mask\' but head_attr.ignore is {head_attr["ignore"]}.')

							# 'unsure' does not happen without 'ignore'.
							if unsure != 0:
								print(f'\t[{box_id}] head_attr.unsure is {head_attr["unsure"]}.')
						else:
							#
							# "head_attr": "unsure": 1 case
							#
							if unsure != 0:
								print(f'\t### [{box_id}] \'head_attr.ignore\' is {ignore} but head_attr.unsure is {unsure}.')
								sys.exit(1)

			n += 1

		print(f'checked {n} items.\n')

def usage():
	print(f'usage: python {__file__} filename')

if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()
	else:
		convert(sys.argv[1:])
