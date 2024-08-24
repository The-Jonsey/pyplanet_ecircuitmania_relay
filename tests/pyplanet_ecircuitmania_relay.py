import asyncio
import os
import sys
import unittest

from thejonsey.pyplanet_ecircuitmania_relay import PyplanetECircuitmaniaRelayApp

from pyplanet.core import Controller

from unittest.mock import MagicMock

from types import SimpleNamespace




class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class PyplanetECircuitmaniaRelayAppTests(unittest.TestCase):
    app: PyplanetECircuitmaniaRelayApp = None

    instance: Controller

    @classmethod
    def setUp(self):
        PyplanetECircuitmaniaRelayApp.path = os.curdir
        self.instance = MagicMock()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.app = PyplanetECircuitmaniaRelayApp("thejonsey.pyplanet_ecircuitmania_relay.app", "thejonsey.pyplanet_ecircuitmania_relay", self.instance)

    def test_start_invalid_token(self):
        @asyncio.coroutine
        async def go():
            self.app.instance.chat = AsyncMock()
            player = "mock_player"
            await self.app.start(player, SimpleNamespace(**{"token": "adwdawd"}))
            self.assertEqual(self.app.matchId, "")
            self.assertEqual(self.app.token, "")
            self.app.instance.chat.assert_called_with("Invalid token", player)
        self.loop.run_until_complete(go())

    def test_start_valid_token(self):
        @asyncio.coroutine
        async def go():
            self.app.instance.chat = AsyncMock()
            player = "mock_player"
            await self.app.start(player, SimpleNamespace(**{"token": "adwdawd_badwad"}))
            self.assertEqual(self.app.matchId, "adwdawd")
            self.assertEqual(self.app.token, "badwad")
            self.app.instance.chat.assert_called_with("E-Circuitmania connection activated")
        self.loop.run_until_complete(go())




if __name__ == '__main__':
    unittest.main()
