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
from typing import Optional

from pyrogram import emoji


async def format_section(key, section: list) -> Optional[str]:
    title = key.replace('_', ' ').title()
    content = []
    if not section:
        return
    for entry in section:
        item = "- {percent:>5}% {time:>5} {name}".format(
            percent=format(entry['percent'], '.2f'),
            time=f"{entry['hours']:02d}:{entry['minutes']:02d}",
            name=entry['name']
        )
        content.append(item)
    content = "\n".join(content)
    return f"**{title}**:\n```{content}```"


async def format_wakatime_stats(stats: dict):
    days_count = stats['days_including_holidays']
    result = [
        "**{} {} Day{} of WakaTime Stats for {}**".format(
            emoji.CHART_INCREASING,
            days_count,
            's' if days_count > 1 else '',
            stats['username']
        )
    ]
    for key, value in stats.items():
        if type(value) == list:
            section = await format_section(key, value)
            if section:
                result.append(section)
    return "\n\n".join(result)


async def main():
    with open('wakatime.json') as f:
        stats: dict = json.load(f)['data']
    formatted_stats = await format_wakatime_stats(stats)
    print(formatted_stats)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
