import sys
#from import pathlib
#import pathlib.PurePath
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
#				print(aitem)
#				print(type(aitem))
#				print(x)
#				wf.write(x)
#				wf.write('\n')
				wf.write(f'[{n}]\n')
				n += 1

				wf.write('ID:' + aitem['ID'] + '\n')
#				wf.write('"gtboxes":' + str(aitem['gtboxes']) + '\n')
				#for i, (k, v) in enumerate (aitem['gtboxes'].items()):
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

	#convert()
	#print(__file__)
	#print(type(__file__))
