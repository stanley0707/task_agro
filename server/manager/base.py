class BaseManager:
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		return isinstance(exc_val, TypeError)

	async def __aenter__(self):
		return self
	
	async def __aexit__(self, exc_type, exc_val, exc_tb):
		return isinstance(exc_val, TypeError)
	
	async def __await__(self):
		return self