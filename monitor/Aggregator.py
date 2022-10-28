import dataclasses



@dataclasses.dataclass(frozen=True)
class Aggregator:

	last_error_result: dict[str, list | int | Exception] = dataclasses.field(default_factory=dict)

	def __call__(self, url: str, result: list | int | Exception) -> bool:

		if type(result) == list:

			if url not in self.last_error_result:
				return False

			del self.last_error_result[url]

		else:

			if url in self.last_error_result:
				if self.last_error_result[url] == result:
					return False

			self.last_error_result[url] = result

		return True