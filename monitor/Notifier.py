import dataclasses
from drunk_snail import Template

from .AsyncClient import AsyncClient



@dataclasses.dataclass
class Notifier:

	token: bytes
	chat_id: bytes

	client: AsyncClient

	_last_error_result: dict[str, list | int | Exception] = dataclasses.field(default_factory=dict)

	async def __call__(self, url: str, result: list | int | Exception) -> None:

		message = b''

		if type(result) == list:

			if url not in self._last_error_result:
				return

			del self._last_error_result[url]
			message = Template('MessageOk')({
				'url': url.encode()
			})

		else:

			if url in self._last_error_result:
				if self._last_error_result[url] == result:
					return

			self._last_error_result[url] = result
			message = Template('MessageError')({
				int: {
					'BadReply': {
						'status_code': str(result).encode()
					}
				},
				Exception: {
					'Exception': {
						'text': str(result).encode()
					}
				}
			}[type(result)])

		await self.client.get(
			Template('RequestUrl')({
				'token': self.token,
				'chat_id': self.chat_id,
				'Message': message
			}).decode()
		)