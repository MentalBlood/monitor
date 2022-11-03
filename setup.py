import glob
from setuptools import setup, find_packages



if __name__ == '__main__':

	setup(

		name='monitor',
		version='1.0.0',
		description='Tool for services monitoring (pinging)',
		author='mentalblood',

		python_requires='>=3.10',
		install_requires=[
			'httpx',
			'py-notifier',
			'drunk_snail'
		],

		packages=find_packages(),
		package_data={'templates': glob.glob('monitor/templates/*')},
		include_package_data=True

	)
