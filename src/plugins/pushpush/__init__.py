from nonebot import get_plugin_config, on_command
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message, Bot, GroupMessageEvent, MessageSegment

from nonebot.params import CommandArg

from .config import Config
from .models.pushgroup import PushGroup
from .models.pushperson import PushPerson

import requests

__plugin_meta__ = PluginMetadata(
    name="pushpush",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

push = on_command("push", rule = to_me())

@push.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    omsg = event.original_message
    argv = omsg[1].data["text"].split()
    if len(argv) <= 1:
        await push.send("参数错误")
        return

    if argv[1] == "on":
        if len(omsg) == 2:
            await push_group_turn_on(event.group_id)
            await push.send("本群加训模式已开启")
        elif len(omsg) == 3 and omsg[2].type == "at":
            person_id = omsg[2].data["qq"]
            ok = await push_person_turn_on(person_id)
            if ok:
                await push.send(Message([MessageSegment.text("成功将"), MessageSegment.at(person_id), MessageSegment.text(" 加入加训列表")]))
            else:
                await push.send("请先使用 /push bind @xxx cf_username 来绑定 cf 账号")
        else:
            await push.send("参数错误")
    elif argv[1] == "off":
        if len(omsg) == 2:
            await push_group_turn_off(event.group_id)
            await push.send("本群加训模式已关闭")
        elif len(omsg) == 3 and omsg[2].type == "at":
            person_id = omsg[2].data["qq"]
            ok = await push_person_turn_off(person_id)
            if ok:
                await push.send(Message([MessageSegment.text("成功将"), MessageSegment.at(person_id), MessageSegment.text(" 移除加训列表")]))
            else:
                await push.send("请先使用 /push bind @xxx cf_username 来绑定 cf 账号")
        else:
            await push.send("参数错误")
    elif argv[1] == "bind":
        if not check_bind(omsg):
            await push.send("参数错误")
            return
        person_id = omsg[2].data["qq"]
        cf_username = omsg[3].data["text"].split()[0]
        if not check_username(cf_username):
            await push.send("不存在的 cf 用户或获取用户信息失败")
            return
        await push_bind(person_id, cf_username)
        await push.send("绑定 codeforces 账号成功")

def check_bind(omsg):
    return len(omsg) == 4 and omsg[2].type == "at"

def check_username(username):
    url = "https://codeforces.com/api/user.info?handles=" + username
    resp = requests.get(url)
    if resp.status_code != 200:
        return False
    return resp.json()["status"] == "OK"

async def push_group_turn_on(group_id):
    if group := await PushGroup.filter(id = group_id).first():
        group.open = True
        await group.save()
    else:
        await PushGroup.create(id = group_id, open = True)

async def push_group_turn_off(group_id):
    if group := await PushGroup.filter(id = group_id).first():
        group.open = False
        await group.save()
    else:
        await PushGroup.create(id = group_id, open = False)

async def push_bind(person_id, cf_username):
    if person := await PushPerson.filter(id = person_id).first():
        person.cf_username = cf_username
        await person.save()
    else:
        await PushPerson.create(id = person_id, cf_username = cf_username, open = True)

async def push_person_turn_on(person_id):
    if person := await PushPerson.filter(id = person_id).first():
        person.open = True
        await person.save()
        return True
    else:
        return False
    
async def push_person_turn_off(person_id):
    if person := await PushPerson.filter(id = person_id).first():
        person.open = False
        await person.save()
        return True
    else:
        return False
    