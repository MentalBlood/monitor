import dataclasses
from drunk_snail import Template

from .AsyncClient import AsyncClient



@dataclasses.dataclass(frozen=True)
class Notifier:

	token: bytes
	chat_id: bytes

	client: AsyncClient

	async def __call__(self, url: str, result: list | int | Exception) -> None:

		if type(result) == list:
			return

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

		request_url = Template('RequestUrl')({
			'token': self.token,
			'chat_id': self.chat_id,
			'Message': {
				'url': url.encode(),
			} | message_additional_args
		}).decode()

		response = await self.client.get(request_url)
		print(f'{request_url} -> {response}')