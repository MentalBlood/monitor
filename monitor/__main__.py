import os
import asyncio
import argparse

from .Scanner import Scanner
from .Notifier import Notifier
from .Aggregator import Aggregator
from .AsyncClient import AsyncClient
from .notifiers.WindowsNotifier import WindowsNotifier
from .notifiers.TelegramNotifier import TelegramNotifier

from .loadTemplates import loadTemplates
from .MessageComposer import MessageComposer



parser = argparse.ArgumentParser(description='Service for services monitoring')

parser.add_argument(
	'address',
	nargs='+',
	help='Addresses to ping'
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
	'--templates_path',
	'-T',
	type=str,
	default=None,
	help='Templates directory path',
	required=False
)

parser.add_argument(
	'--token',
	'-t',
	type=str,
	default=None,
	help='Telegram bot token',
	required=False
)
parser.add_argument(
	'--chat_id',
	'-c',
	type=str,
	default=None,
	help='Telegram chat id',
	required=False
)

args = parser.parse_args()


async def main(scanners: list[Scanner]):
	await asyncio.gather(*[
		s()
		for s in scanners
	])


loadTemplates(
	args.templates_path or
	os.path.join(
		os.path.dirname(
			os.path.realpath(__file__)
		),
		'templates'
	)
)

notifiers: list[Notifier] = [
	WindowsNotifier(
		client=AsyncClient(args.proxy),
		message_composer=MessageComposer(),
		aggregator=Aggregator(
			validator=lambda r: (type(r) == list) or (r == 403)
		)
	)
]
if args.token and args.chat_id:
	notifiers.append(
		TelegramNotifier(
			client=AsyncClient(args.proxy),
			message_composer=MessageComposer(),
			aggregator=Aggregator(
				validator=lambda r: (type(r) == list) or (r == 403)
			),
			token=args.token.encode(),
			chat_id=args.chat_id.encode(),
		)
	)


try:

	asyncio.run(
		main=main(
			scanners=[
				Scanner(
					url=a,
					interval=args.interval,
					notifiers=notifiers,
					client=AsyncClient(args.proxy)
				)
				for a in args.address
			]
		)
	)

except KeyboardInterrupt:
	exit()