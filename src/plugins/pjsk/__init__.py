from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message
from nonebot_plugin_alconna.uniseg import UniMessage

import math
from nonebot_plugin_pjsk.__main__ import format_draw_error
from nonebot_plugin_pjsk.resource import select_or_get_random
from nonebot_plugin_pjsk.render import (
    DEFAULT_LINE_SPACING,
    DEFAULT_STROKE_COLOR,
    DEFAULT_STROKE_WIDTH,
    get_sticker,
    make_sticker_render_kwargs,
)
from nonebot_plugin_pjsk.utils import resolve_value

from .config import Config

import re

__plugin_meta__ = PluginMetadata(
    name="pjsk",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

def separate_letters_numbers(s):
    letters = re.findall('[A-Za-z]+', s)
    numbers = re.findall('[0-9]+', s)
    return ''.join(letters).lower(), ''.join(numbers)

characters = ["airi", "akito", "an", "emu", "ena", "haruka", "honami", "ichika", "kaito", "kanade", "kohane", "len", "luka", "mafuyu", "meiko", "miku", "minori", "mizuki", "nene", "rin", "rui", "saki", "shiho", "shizuku", "touya", "tsukasa"]
characount = [13, 13, 13, 13, 13, 13, 15, 15, 13, 14, 14, 14, 13, 14, 13, 13, 14, 14, 13, 13, 16, 15, 15, 13, 15, 15]

'''
airi 13
akito 13
an 13
emu 13
ena 13
haruka 13
honami 15
ichika 15
kaito 13
kanade 14
kohane 14
len 14
luka 13
mafuyu 14
meiko 13
miku 13
minori 14
mizuki 14
nen 13
rin 13
rui 16
saki 15
shiho 15
shizuku 13
touya 15
tsukasa 15
'''

pjsk = on_command("pjsk", priority = 1)

@pjsk.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if msgtext := args.extract_plain_text():
        msgtexts = msgtext.split(' ', 1)
        char_and_id = msgtexts[0]
        content = '' if len(msgtexts) == 1 else msgtexts[1]
        character, idstr = separate_letters_numbers(char_and_id)
        if character not in characters:
            matcher.skip()
        if idstr == '':
            matcher.skip()
        idnum = int(idstr)
        total = 0
        for i in range(0, 26):
            if characters[i] == character:
                if idnum > characount[i]:
                    await matcher.send("错误的表情 ID")
                    matcher.stop_propagation()
                    await matcher.finish()
                break
            total += characount[i]
        idnum += total

        selected_sticker = select_or_get_random(str(idnum))
        default_text = selected_sticker.default_text
        try:
            kw = make_sticker_render_kwargs(
                selected_sticker,
                text=content,
                x=default_text.x,
                y=default_text.y,
                rotate=math.degrees(default_text.r / 10),
                font_size=default_text.s,
                font_color=selected_sticker.color,
                stroke_width=DEFAULT_STROKE_WIDTH,
                stroke_color=DEFAULT_STROKE_COLOR,
                line_spacing=DEFAULT_LINE_SPACING,
                auto_adjust=True,
            )
            image = await get_sticker(**kw)
        except Exception as e:
            await matcher.finish(format_draw_error(e))

        await UniMessage.image(raw=image).send(reply_to=True)
        matcher.stop_propagation()