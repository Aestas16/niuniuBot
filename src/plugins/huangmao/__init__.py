from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment

from .config import Config

import os
import random
from pathlib import Path

__plugin_meta__ = PluginMetadata(
    name="huangmao",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

huangmao = on_command("来点黄毛", rule = to_me())

@huangmao.handle()
async def handle_function():
    rint = random.randint(1, 179)
    cdnurl = "https://raw.githubusercontent.com/Aestas16/niuniuBot/refs/heads/huangmao/"
    imgurl = cdnurl
    if rint <= 2:
        imgurl += f'{rint}.webp'
    elif rint <= 3:
        rint -= 2
        imgurl += f'{rint}.gif'
    elif rint <= 112:
        rint -= 3
        imgurl += f'{rint}.jpg'
    elif rint <= 177:
        rint -= 112
        imgurl += f'{rint}.png'
    else:
        rint -= 177
        imgurl += f'{rint}.jpeg'
    print(imgurl)
    await huangmao.send(MessageSegment.image(imgurl))

'''
webp 2
gif 1
jpg 109
png 65
jpeg 2
'''