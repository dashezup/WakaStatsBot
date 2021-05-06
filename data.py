"""
WakaStatsBot, Telegram bot for sharing WakaTime stats
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import asyncio
import json

from aiohttp import ClientSession


# from aiohttp_socks import ProxyConnector


async def get_session() -> ClientSession:
    # connector = ProxyConnector.from_url('socks5://127.0.0.1:1080')
    # return ClientSession(connector=connector)
    return ClientSession()


session: ClientSession \
    = asyncio.get_event_loop().run_until_complete(get_session())

try:
    with open('userdata.json') as f:
        userdata = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    userdata = {}
