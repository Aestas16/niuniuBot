from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_fullmatch

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="slecy",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

slecy = on_fullmatch("slecy")

@slecy.handle()
async def handle_function():
    await slecy.send("slecy")