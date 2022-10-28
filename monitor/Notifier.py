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

		if type(result) == list:

			if url in self._last_error_result:

				del self._last_error_result[url]

				response = await self.client.get(
					Template('RequestUrl')({
						'token': self.token,
						'chat_id': self.chat_id,
						'MessageOk': {
							'url': url.encode()
						}
					}).decode()
				)
				print(f'{url} is OK -> {response}')

		else:

			if url in self._last_error_result:
				if self._last_error_result[url] == result:
					return

			self._last_error_result[url] = result

			message_additional_args = {}
			if type(result) == int:
				message_additional_args = {
					'BadReply': {
						'status_code': str(result).encode()
					}
				}
			elif type(result) == Exception:
				message_additional_args = {
					'Exception': {
						'text': str(result).encode()
					}
				}

			response = await self.client.get(
				Template('RequestUrl')({
					'token': self.token,
					'chat_id': self.chat_id,
					'MessageError': {
						'url': url.encode(),
					} | message_additional_args
				}).decode()
			)
			print(f'{url} is NOT OK -> {response}')