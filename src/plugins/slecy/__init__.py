from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_fullmatch, on_keyword

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="slecy",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

slecy = on_fullmatch("slecy")

slecy_keyword = on_keyword({"水7", "ppp", "缪", "声优", "你水", "跑活", "抽选", "水团", "小偶像", "aqours", "Aqours", "fmt", "莲团", "星团", "二偶"})

@slecy.handle()
async def handle_function():
    await slecy.send("slecy")

@slecy_keyword.handle()
async def handle_function_keyword():
    await slecy.send("slecy")