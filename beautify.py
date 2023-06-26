#
# convert annotation_train.odgt and annotation_val.odgt 
# from https://www.crowdhuman.org into easy format 
# for human reading.
#

# beauty.py

# copyright jay.nam@openstack.co.kr

import sys
from pathlib import PurePath
import json

def convert(argv):
	for x in argv:
		print(x)

	with open(argv[0], 'r') as rf:
		p = PurePath(argv[0])
		with open(p.stem + '.txt', 'w') as wf:

			n = 0
			
			for x in rf:
				aitem = json.loads(x)
				wf.write(f'[{n}]\n')
				n += 1

				wf.write('ID:' + aitem['ID'] + '\n')
				i = 0
				for af in aitem['gtboxes']:
#					wf.write(f'{str(af)} \n')
					wf.write(f'{[i]}')
					wf.write(f'{{tag: {af["tag"]}')
					wf.write(f',\textra: {af["extra"]}')
					wf.write(f',\thbox: {af["hbox"]}')
					wf.write(f',\thead_attr: {af["head_attr"]}')
					wf.write(f',\tvbox: {af["vbox"]}')
					wf.write(f',\tfbox: {af["fbox"]}}}\n')

					i += 1

				wf.write('\n')

def usage():
	print(f'usage: python {__file__} filename')

if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()
	else:
		convert(sys.argv[1:])
