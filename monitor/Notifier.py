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

	@abc.abstractmethod
	async def __call__(self, url: str, result: list | int | Exception) -> None:
		pass