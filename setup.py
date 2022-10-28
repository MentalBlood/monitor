from setuptools import setup, find_packages



if __name__ == '__main__':

	setup(
		name='monitor',
		version='1.0.0',
		description='Tool for services monitoring (pinging)',
		python_requires='>=3.10',
		packages=find_packages()
	)
