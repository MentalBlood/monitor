import httpx
import asyncio
import argparse
import platform
from typing import Callable



parser = argparse.ArgumentParser(description='Service for services monitoring')

parser.add_argument(
	'ip',
	nargs='+',
	help='IP addresses of services to ping'
)
parser.add_argument(
	'-p',
	'--proxy',
	type=str,
	default=None,
	help='Proxy address',
	required=False
)
parser.add_argument(
	'--interval',
	'-i',
	type=float,
	default=1.0,
	help='Ping interval in seconds',
	required=False
)

args = parser.parse_args()


client = httpx.AsyncClient(proxies=f'http://{args.proxy}')


async def ping(
	url: str,
	interval: float,
	callback: Callable = lambda url, result: print(url, result)
) -> list | int | Exception:

	while True:

		result = None

		try:

			response = await client.get(url)

			if response.status_code == 200:
				result = response.json()
			else:
				result = response.status_code

		except Exception as e:
			result = e

		callback(url, result)

		await asyncio.sleep(interval)


async def main(ips):

	await asyncio.gather(*[
		ping(f'http://{ip}/services', args.interval)
		for ip in ips
	])


if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main(args.ip))