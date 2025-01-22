from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment,
    MessageEvent,
    PrivateMessageEvent,
)
from typing import Union

from .config import Config

import requests

__plugin_meta__ = PluginMetadata(
    name="setu",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

setu = on_command("setu", rule = to_me())

@setu.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    resp = requests.get("https://api.lolicon.app/setu/v2?excludeAI=true")
    if resp.status_code == 200:
        res = resp.json()
        url = res["data"][0]["urls"]["original"]
        messages = [
            {
                "type": "node",
                "data": {
                    "name": "牛牛",
                    "uin": 2377845646,
                    "content": [{
                        "type": "image",
                        "data": {
                            "file": url
                        }
                    }]
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "牛牛",
                    "uin": 2377845646,
                    "content": [{
                        "type": "text",
                        "data": {
                            "text": url
                        }
                    }]
                }
            }
        ]
        if isinstance(event, GroupMessageEvent):
            await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
        else:
            await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)