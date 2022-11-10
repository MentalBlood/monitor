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
			if type(result) == list:
				pass
			elif type(result) == int:
				return Template('MessageError')({
					'BadReply': {
						'status_code': str(result).encode()
					}
				})
			else:
				return Template('MessageError')({
					'Exception': {
						'text': str(result).encode()
					}
				})