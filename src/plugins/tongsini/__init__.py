from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_keyword

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="tongsini",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

tongsini = on_keyword({"捅死你", "tongsini"})
tsn = on_command("tsn")

@tongsini.handle()
async def handle_function():
    await tongsini.send("等一下，刚才跟你讲话的人是谁？我不是早就警告过你不要乱跟别人说话了吗？为什么你还是不听我的？为什么你每天都在跟别人一起聊天也不来找我？ 你知道我每天盯着聊天框等着新消息有多难受吗？为什么不来找我？是因为别人长得比我好看吗？你看腻我了？还是觉得我性格不好？我讲话很难听？觉得我很烦？我明明已经努力忍着不烦你了，我一直在等着你给我发消息，为什么你却天天把我晾在一边？你为什么要疏远我？是不是她跟你关系太好了？为什么你的眼里只有别人没有我？别人到底哪里比我好了？我要捅死你！！！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！")

@tsn.handle()
async def handle_function():
    await tsn.send("等一下，刚才跟你讲话的人是谁？我不是早就警告过你不要乱跟别人说话了吗？为什么你还是不听我的？为什么你每天都在跟别人一起聊天也不来找我？ 你知道我每天盯着聊天框等着新消息有多难受吗？为什么不来找我？是因为别人长得比我好看吗？你看腻我了？还是觉得我性格不好？我讲话很难听？觉得我很烦？我明明已经努力忍着不烦你了，我一直在等着你给我发消息，为什么你却天天把我晾在一边？你为什么要疏远我？是不是她跟你关系太好了？为什么你的眼里只有别人没有我？别人到底哪里比我好了？我要捅死你！！！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！捅死你！")