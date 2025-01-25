from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .config import Config
from .generator import genImage

import base64
from io import BytesIO

__plugin_meta__ = PluginMetadata(
    name="5k",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

five = on_command("5k", rule = to_me())

@five.handle()
async def handle_function(args: Message = CommandArg()):
    if msgtext := args.extract_plain_text():
        if "|" in msgtext:
            word_a = msgtext.split("|")[0]
            word_b = msgtext.split("|")[1]
            buf = BytesIO()
            genImage(word_a, word_b).save(buf, format="PNG")
            img_str = "base64://" + base64.b64encode(buf.getvalue()).decode()
            await five.finish(MessageSegment.image(img_str))
        else:
            await five.finish("参数错误。用法：5k <第一句>|<第二句>")
    else:
        await five.finish("参数错误。用法：5k <第一句>|<第二句>")