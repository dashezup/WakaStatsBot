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
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiohttp import ClientResponse
from data import session, userdata


@Client.on_message(filters.text
                   & filters.incoming
                   & ~filters.edited
                   & filters.command("start"))
async def command_start(_, m: Message):
    text = (
        "**This bot allows you to get and share your "
        "WakaTime/Wakapi stats**\n\n"
        "Use **/api [url]** command to set or check API URL, send it as a "
        "reply to any message to remove your API URL settings. Make sure the "
        "API URL response with proper JSON data before set it.\n\n"
        "**WakaTime API URL**:\n"
        "`https://wakatime.com/api/v1/users/{username}/stats/last_7_days`\n\n"
        "**Wakapi API URL**:\n"
        "`https://wakapi.dev/api/v1/users/{username}/stats/last_7_days`\n\n"
        "[Source Code](https://github.com/dashezup/WakaStatsBot)"
        " | [Developer](https://t.me/dashezup)"
        " | [Support Chat](https://t.me/ezupdev)"
    )
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Select a Chat to Try Inline",
                    switch_inline_query=""
                )
            ],
            [
                InlineKeyboardButton(
                    "Try Inline in This Chat",
                    switch_inline_query_current_chat=""
                )
            ]
        ]
    )
    await m.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Client.on_message(filters.text
                   & filters.incoming
                   & ~filters.edited
                   & filters.command("api"))
async def set_api_url(_, m: Message):
    user_id = m.from_user.id
    if m.reply_to_message:
        userdata.pop(str(user_id), None)
        await m.reply_text("Your API URL setting has been removed", quote=True)
        return
    len_cmd = len(m.command)
    if len_cmd == 1:
        await m.reply_text(userdata.get(str(user_id),
                                        "You didn't set API URL yet"))
        return
    if len_cmd == 2 and m.command[1].startswith("https://"):
        url = m.command[1]
        validation: bool = await validate_url(url)
        if validation:
            userdata[str(user_id)] = url
            await m.reply_text(f"Your API URL has been set to: {url}",
                               quote=True)
            return
    await m.reply_text("Invalid URL", quote=True)


async def validate_url(url: str) -> bool:
    try:
        async with session.get(url) as resp:  # type: ClientResponse
            if resp.status == 200:
                return True
        return False
    except ConnectionResetError:
        return False
