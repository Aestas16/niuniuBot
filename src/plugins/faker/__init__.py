from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import CommandArg
from typing import Union
import re

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="faker",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

async def checkatxxxsay(event: GroupMessageEvent) -> bool:
    if len(event.original_message) > 1 and event.original_message[0].type == "at":
        if event.original_message[1].data.get("text").strip().startswith("say"):
            return True
    return False

atxxxsay = on_message(rule = checkatxxxsay, block = True)
@atxxxsay.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    omsg = event.original_message
    xxx = omsg[0].data["qq"]
    omsg[1] = str(omsg[1]).split("say ")[1]
    xxx_group_info = await bot.get_group_member_info(group_id = event.group_id, user_id = int(xxx), no_cache = False)
    msg = omsg[1:]
    messages = [{
        "type": "node",
        "data": {
            "name": xxx_group_info["nickname"] if xxx_group_info["card"] == "" else xxx_group_info["card"],
            "uin": int(xxx),
            "content": msg
        },
    }]
    await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)

async def checkxxxsay(event: Union[PrivateMessageEvent, GroupMessageEvent]) -> bool:
    if event.original_message[0].type == "text" and re.match(r"^\d{6,10} say", event.original_message[0].data.get("text")):
        return True
    return False

xxxsay = on_message(rule = checkxxxsay, block = True)
@xxxsay.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    omsg = event.original_message
    xxx = str(omsg[0]).split(" say ")[0]
    omsg[0] = str(omsg[0]).split(" say ")[1]
    xxx_info = await bot.get_stranger_info(user_id = int(xxx), no_cache = False)
    msg = omsg[0:]
    messages = [{
        "type": "node",
        "data": {
            "name": xxx_info["nickname"],
            "uin": int(xxx),
            "content": msg
        },
    }]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)

lxjsay = on_command("lxj say")
@lxjsay.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    messages = [{
        "type": "node",
        "data": {
            "name": "Rigel",
            "uin": 936641716,
            "content": args
        },
    }]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)

hztsay = on_command("hzt say")
@hztsay.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    messages = [{
        "type": "node",
        "data": {
            "name": "Sisyphe",
            "uin": 1767890287,
            "content": args
        },
    }]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)

ljhsay = on_command("ljh say")
@ljhsay.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    messages = [{
        "type": "node",
        "data": {
            "name": "Konjac16",
            "uin": 793270758,
            "content": args
        },
    }]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)

gzysay = on_command("gzy say")
@gzysay.handle()
async def handle_function(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    messages = [{
        "type": "node",
        "data": {
            "name": "__stick",
            "uin": 1602427689,
            "content": args
        },
    }]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api("send_group_forward_msg", group_id = event.group_id, messages = messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id = event.user_id, messages = messages)