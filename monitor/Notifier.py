import abc
import dataclasses

from .Aggregator import Aggregator
from .AsyncClient import AsyncClient
from .MessageComposer import MessageComposer



@dataclasses.dataclass
class Notifier(abc.ABC):

	client: AsyncClient
	message_composer: MessageComposer

	aggregator: Aggregator

	async def __call__(self, url: str, result: list | int | Exception) -> None:
		if self.aggregator(url, result):
			return await self._call(url, result)

	@abc.abstractmethod
	async def _call(self, url: str, result: list | int | Exception) -> None:
		pass