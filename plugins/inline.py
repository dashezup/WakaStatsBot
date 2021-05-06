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
from aiohttp import ClientResponse
from aiohttp.client_exceptions import ContentTypeError
from pyrogram import Client, filters, emoji
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)

from data import session, userdata
from utils.wakatime import format_wakatime_stats


@Client.on_inline_query()
async def answer_iq(_, iq: InlineQuery):
    results = [
        InlineQueryResultArticle(
            title=f"{emoji.CHART_INCREASING} WakaTime Stats",
            input_message_content=InputTextMessageContent(
                "**Press the button below to load your WakaTime stats**"
            ),
            description="Supports WakaTime/Wakapi API",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"{emoji.CHART_INCREASING} Get WakaTime Stats",
                            callback_data="get_wakatime_stats"
                        )
                    ]
                ]
            )
        ),
        InlineQueryResultArticle(
            title=f"{emoji.INFORMATION} About the Bot",
            input_message_content=InputTextMessageContent(
                f"{emoji.ROBOT} **WakaTime Stats Bot** (@WakaStatsBot)\n\n"
                "__Share your WakaTime/Wakapi statistics "
                "through inline mode__\n\n"
                "**License**: AGPL-3.0-or-later\n"
                "**[Source Code](https://github.com/dashezup/WakaStatsBot)"
                " | [Developer](https://t.me/dashezup)"
                " | [Support Chat](https://t.me/ezupdev)**",
                disable_web_page_preview=True
            ),
            description="Open-source bot made by Dash Eclipse (@dashezup)",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Try @WakaStatsBot",
                            switch_inline_query_current_chat=""
                        )
                    ]
                ]
            )
        )
    ]
    await iq.answer(results)


@Client.on_callback_query(filters.regex("^get_wakatime_stats$"))
async def get_wakatime_stats(_, cq: CallbackQuery):
    url = userdata.get(str(cq.from_user.id))
    if not url:
        await replace_text_and_button(cq)
        await cq.answer("You need to configure API URL in PM at first")
        return
    try:
        async with session.get(url) as resp:  # type: ClientResponse
            if resp.status != 200:
                raise ValueError
            json_resp = await resp.json()
            formatted_stats = await format_wakatime_stats(json_resp['data'])
        await cq.edit_message_text(formatted_stats)
    except (ContentTypeError, KeyError, ValueError):
        await replace_text_and_button(cq)
        await cq.answer(
            "Something went wrong while fetching JSON data from your API URL, "
            "you may change the API URL with /api command in PM",
            show_alert=True
        )


async def replace_text_and_button(cq: CallbackQuery):
    await cq.edit_message_text(
        "**WakaTime Stats Bot**\n"
        "Supports WakaTime/Wakapi API",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Set Your API URL in Private",
                        url="https://t.me/WakaStatsBot?start="
                    )
                ]
            ]
        )
    )
