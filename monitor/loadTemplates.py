import os
import glob
from drunk_snail import Template



def loadTemplates(dir_path: str, encoding: str='utf8') -> None:
	for p in glob.iglob(os.path.join(dir_path, '*')):
		with open(p, 'r', encoding=encoding) as f:
			Template(
				os.path.splitext(
					os.path.basename(p)
				)[0]
			).register(
				f.read()
			)