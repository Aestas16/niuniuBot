import datetime
import logging
from nonebot import get_plugin_config, on_command
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata

from .config import Config
import requests

__plugin_meta__ = PluginMetadata(
    name="cf",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

cf = on_command("cf", rule = to_me(), aliases = {"codeforces", "CF", "Codeforces"})

@cf.handle()
async def handle_function():
    url = "https://codeforces.com/api/contest.list?gym=false"
    resp = requests.get(url)
    if resp.status_code == 200:
        contests = resp.json()
        if "result" not in contests:
            logging.error("result字段不存在")
            return
        contests = contests["result"][::-1]
        msg = ""
        for contest in contests:
            if contest["phase"] != "CODING" and contest["phase"] != "BEFORE":
                continue
            msg += contest["name"] + "\n"
            if contest["phase"] == "CODING":
                msg += "[RUNNING!]\n"
            start_time = contest["startTimeSeconds"]
            msg += datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S") + " 开始\n"
            duration = contest["durationSeconds"]
            msg += "持续 %d h %02d min\n" % (duration // 3600, duration % 3600 // 60)
            msg += "\n"
        if msg == "":
            msg = "近期无 Codeforces 比赛"
        await cf.send(msg)
    else:
        logging.error("获取比赛信息错误(url:%s)" % url)
