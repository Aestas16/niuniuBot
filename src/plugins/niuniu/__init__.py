from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="niuniu",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

niuniu = on_command("牛牛", aliases = {"niuniu", "牛", "🐮", "🐂", "🐄", "这么牛", "折磨牛", "zhemeniu", "zhemoniu"})

@niuniu.handle()
async def handle_function():
    await niuniu.send("牛牛")