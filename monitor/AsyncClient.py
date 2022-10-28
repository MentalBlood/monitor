import httpx
from functools import cache



class AsyncClient(httpx.AsyncClient):

	@cache
	def __new__(cls, proxy: str) -> httpx.AsyncClient:
		return httpx.AsyncClient(proxies=f'http://{proxy}')

	def __init__(self, proxy: str):
		pass