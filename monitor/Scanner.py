import asyncio
import dataclasses

from .Notifier import Notifier
from .AsyncClient import AsyncClient



@dataclasses.dataclass(frozen=True)
class Scanner:

	url: str
	interval: float
	notifiers: list[Notifier]

	client: AsyncClient

	async def __call__(self) -> None:

		while True:

			result = None

			try:

				response = await self.client.get(self.url)

				if response.status_code == 200:
					result = response.json()
				else:
					result = response.status_code

			except Exception as e:
				result = e

			for n in self.notifiers:
				await n(self.url, result)

			await asyncio.sleep(self.interval)