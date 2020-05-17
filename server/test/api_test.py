from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

class MyAppTestCase(AioHTTPTestCase):

    @unittest_run_loop
    async def test_example(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        assert "Hello, world" in text


    def test_example_vanilla(self):
        async def test_get_route():
            url = "/"
            resp = await self.client.request("GET", url)
            assert resp.status == 200
            text = await resp.text()
            assert "Hello, world" in text

        self.loop.run_until_complete(test_get_route())