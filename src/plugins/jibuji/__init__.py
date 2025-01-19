from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_keyword, on_fullmatch

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="jibuji",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

ji_keyword = on_keyword({"急了", "jile", "jiji", "急急", "好急", "急死", "有点急"})
ji_fullmatch = on_fullmatch("急")
bieji_keyword = on_keyword({"别急", "bieji"})

@ji_keyword.handle()
async def handle_function():
    await ji_keyword.send("你先别急")
@ji_fullmatch.handle()
async def handle_function():
    await ji_fullmatch.send("你先别急")
@bieji_keyword.handle()
async def handle_function():
    await bieji_keyword.send("急急急急急急急急急急急急急急急急")
