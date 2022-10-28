import dataclasses
from drunk_snail import Template

from .Notifier import Notifier



@dataclasses.dataclass
class TelegramNotifier(Notifier):

	token: bytes
	chat_id: bytes

	async def __call__(self, url: str, result: list | int | Exception) -> None:

		if self.aggregator(url, result):

			await self.client.get(
				Template('RequestUrl')({
					'token': self.token,
					'chat_id': self.chat_id,
					'Message': self.message_composer(url, result)
				}).decode()
			)