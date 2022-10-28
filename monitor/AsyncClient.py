import httpx
from functools import cache



class AsyncClient(httpx.AsyncClient):

	def __init__(self, proxy: str) -> None:
		super().__init__(proxies=f'http://{proxy}')


@cache
def getAsyncClient(proxy: str) -> AsyncClient:
	return AsyncClient(proxy)