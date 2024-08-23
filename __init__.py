import logging

import requests

from pyplanet.apps.config import AppConfig

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.apps.core.maniaplanet.models.player import Player

from pyplanet.contrib.command import Command

logger = logging.getLogger(__name__)


class PyplanetECircuitmaniaRelayApp(AppConfig):
    game_dependencies = ["trackmania_next"]
    app_dependencies = ["core.maniaplanet", "core.trackmania"]
    namespace = "ecm"

    roundNo = 1
    matchId = ""
    token = ""

    startPerm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_init(self):
        await super().on_init()

    async def on_start(self):
        await super().on_start()
        self.context.signals.listen(mp_signals.flow.round_start, self.round_start)
        self.context.signals.listen(tm_signals.scores, self.scores)
        self.context.signals.listen(mp_signals.flow.match_end, self.match_end)
        self.context.signals.listen(mp_signals.flow.server_end, self.server_end)
        self.startPerm = await self.instance.permission_manager.register("start", description="Start ECM connection", min_level=1, namespace="ecm", app=self)
        await self.instance.command_manager.register(Command(
            namespace="ecm",
            command="start",
            target=self.start,
            admin=True,
            description="Start the connection to ECM",
            perms=["ecm:start"]
        ).add_param(
            "token",
            nargs="1",
            type=str,
            required=True,
            help="The token provided by ECM, probably contains an underscore in the middle"
        ))

    async def on_stop(self):
        await super().on_stop()

    async def on_destroy(self):
        await super().on_destroy()

    async def start(self, player, data, *args, **kwargs):
        if "_" not in data.token:
            await self.instance.chat(f"Invalid token", player)
            return
        parts = data.token.split("_")
        self.matchId = parts[0]
        self.token = parts[1]
        await self.instance.chat(f"E-Circuitmania connection activated")

    async def server_end(self, restarted, time):
        self.matchId = ""
        self.token = ""
        await self.instance.chat(f"E-Circuitmania connection closed")

    async def match_end(self, count, time):
        self.matchId = ""
        self.token = ""
        await self.instance.chat(f"E-Circuitmania connection closed")

    async def round_start(self, count, time, valid):
        self.roundNo = valid

    async def scores(self, players, teams, winner_team, use_teams, winner_player, section):
        if section == "PreEndRound" and self.matchId != "" and self.token != "":
            payload = {"mapId": self.instance.map_manager.current_map.uid, "roundNum": self.roundNo, "players": []}
            for player in players:
                player_real : Player = player["player"]
                if player_real.flow.is_spectator:
                    continue
                logger.info(player)
                payload["players"].append({
                    "ubisoftUid": player['player_account_id'],
                    "finishTime": player['prevracetime'],
                    "position": player['rank']
                })
                # await self.instance.chat(f"{player}")
                await self.instance.chat(f"{self.instance.map_manager.current_map.uid}")
                await self.instance.chat(f"{player['rank']}. {player['player_account_id']}: {player['prevracetime']}")
            logger.info(payload)
            # r = requests.post("https://us-central1-fantasy-trackmania.cloudfunctions.net/match-addRound", params=dict(matchId=self.matchId), json=payload, headers=dict(Authorization=f"Bearer {self.token}"))
            # if r.status_code != 200:
            #     for player in self.instance.player_manager.online:
            #         if self.instance.permission_manager.has_permission(player, self.startPerm):
            #             await self.instance.chat(f"Error with connection to ECM, data-loss may occur", player)

