from aiohttp import web
from manager import ApiManager
from models import Link


async def get_domain(request):
	"""   """
	with ApiManager(Link) as manager:
		# Контекстный менеджер API открывает
		# доступ к базовым методам по работе
		# с данными. Конкретная реализация
		# каждого частоного метода API рекомендуема
		# для реализации в рамках инстанса этого менеджера
		manager.params = request.rel_url.query
		manager.visited_domains()
		return web.json_response(
						manager.response['data'],
						status=manager.status
					)

async def post_urls(request):
	"""   """
	async with ApiManager(Link) as manager:

		manager.request = request
		manager.params = await manager.body_json()
		manager.run(manager.model.save_to_redis)
		return web.json_response(
						manager.response['data'],
						status=manager.status
					)