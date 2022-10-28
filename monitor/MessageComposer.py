import dataclasses
from drunk_snail import Template



@dataclasses.dataclass(frozen=True)
class MessageComposer:

	def __call__(self, url: str, result: list | int | Exception) -> bytes:

		if type(result) == list:
			return Template('MessageOk')({
				'url': url.encode()
			})

		else:
			return Template('MessageError')({
				list: {},
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