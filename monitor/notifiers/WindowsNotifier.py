import dataclasses
from pynotifier import Notification

from ..Notifier import Notifier



@dataclasses.dataclass
class WindowsNotifier(Notifier):

	icon_path: str | None = None

	async def _call(self, url: str, result: list | int | Exception) -> None:

		Notification(
			title=url,
			description=self.message_composer(url, result).decode(),
			icon_path=self.icon_path,
			duration=0
		).send()