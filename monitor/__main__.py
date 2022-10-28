import asyncio
import argparse

from .Scanner import Scanner
from .Notifier import Notifier
from .AsyncClient import getAsyncClient

from .loadTemplates import loadTemplates
from .MessageComposer import MessageComposer



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
parser.add_argument(
	'--token',
	'-t',
	type=str,
	help='Telegram bot token',
	required=True
)
parser.add_argument(
	'--chat_id',
	'-c',
	type=str,
	help='Telegram chat id',
	required=True
)
parser.add_argument(
	'--templates_path',
	'-T',
	type=str,
	help='Templates directory path',
	required=True
)

args = parser.parse_args()



async def main(scanners: list[Scanner]):
	await asyncio.gather(*[
		s()
		for s in scanners
	])


loadTemplates(args.templates_path)


asyncio.run(
	main=main(
		scanners=[
			Scanner(
				url=f'http://{ip}/services',
				interval=args.interval,
				notifier=Notifier(
					token=args.token.encode(),
					chat_id=args.chat_id.encode(),
					client=getAsyncClient(args.proxy),
					message_composer=MessageComposer()
				),
				client=getAsyncClient(args.proxy)
			)
			for ip in args.ip
		]
	)
)