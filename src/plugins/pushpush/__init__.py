from nonebot import get_plugin_config, on_command, require, get_bot
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message, Bot, GroupMessageEvent, MessageSegment
from nonebot_plugin_apscheduler import scheduler
from nonebot.params import CommandArg

from .config import Config
from .models.pushgroup import PushGroup
from .models.pushperson import PushPerson
from .models.pushaccount import PushAccount

import requests
from datetime import timedelta, datetime
import json

require("nonebot_plugin_apscheduler")

__plugin_meta__ = PluginMetadata(
    name="pushpush",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

push = on_command("push", rule = to_me())

@scheduler.scheduled_job("cron", hour = 20, minute = 0)
async def scheduled_day_push():
    groups = await PushGroup.filter(open = True).all()
    bot = get_bot()
    for group in groups:
        await bot.call_api("send_group_msg", group_id = group.id, message = "今天，你加训了吗？以下是群友最近 24 小时 Codeforces 做题情况：")
        await push_with_day(group.id, 1, at = True)

@scheduler.scheduled_job("cron", day_of_week = "sun", hour = 8, minute = 0)
async def scheduled_week_push():
    groups = await PushGroup.filter(open = True).all()
    bot = get_bot()
    for group in groups:
        await bot.call_api("send_group_msg", group_id = group.id, message = "这周你到底加训了没有？以下是群友最近一周 Codeforces 做题情况：")
        await push_with_day(group.id, 1, at = True)

@push.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    omsg = event.original_message
    argv = omsg[1].data["text"].split()
    if argv[1].isdigit():
        await push.send("请稍等...")
        day = int(argv[1])
        await push_with_day(event.group_id, day, at = False)
    elif argv[1] == "on":
        if len(omsg) == 2:
            await push_group_turn_on(event.group_id)
            await push.send("本群加训模式已开启")
        elif len(omsg) == 3 and omsg[2].type == "at":
            person_id = omsg[2].data["qq"]
            ok = await push_person_turn_on(person_id)
            if ok:
                await push.send(Message([MessageSegment.text("成功将"), MessageSegment.at(person_id), MessageSegment.text(" 加入加训列表")]))
            else:
                await push.send("请先使用 push bind 来绑定 cf 账号")
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
                await push.send("请先使用 push bind 来绑定至少一个 cf 账号")
        else:
            await push.send("参数错误")
    elif argv[1] == "bind":
        if not (len(omsg) == 4 and omsg[2].type == "at"):
            await push.send("参数错误")
            return
        person_id = omsg[2].data["qq"]
        cf_username = omsg[3].data["text"].split()[0]
        try:
            if not check_username(cf_username):
                await push.send("获取用户信息失败")
                return
        except Exception as e:
            await push.send(str(e))
            return
        await push_bind(person_id, cf_username)
    elif argv[1] == "unbind":
        if len(argv) != 3:
            await push.send("参数错误")
            return
        cf_username = argv[2]
        await push_unbind(cf_username)
    elif argv[1] == "list":
        members = await bot.get_group_member_list(group_id = event.group_id)
        msg = "加训列表：\n"
        for member in members:
            accounts = await query_person_pushed(member["user_id"])
            if len(accounts) > 0:
                name = member["card"] if len(member["card"]) > 0 else member["nickname"]
                msg += "%s（%s）\n" % (name, "|".join(accounts))
        await push.send(msg)
    elif argv[1] == "help":
        await push.send("push on: 启动本群加训模式\n" +
                        "push off: 关闭本群加训模式\n" +
                        "push on @xxx: 将群友 xxx 加入加训列表\n" +
                        "push off @xxx: 将群友 xxx 移出加训列表\n" +
                        "push bind @xxx [cf_username]: 绑定 xxx 的 Codeforces 账号\n" +
                        "push unbind [cf_username]: 解绑 Codeforces 账号\n" +
                        "push list: 查看加训列表\n" +
                        "push [days]: 查看最近若干天内的 Codeforces 加训情况")
    else:
        await push.send("参数错误")

def check_username(username):
    url = "https://codeforces.com/api/user.info?handles=" + username
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("code %d" % resp.status_code)
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
    
async def push_bind(person_id, cf_username):
    if account := await PushAccount.filter(id = cf_username).first():
        await push.send("该 cf 账号已被绑定过")
        return
    await PushAccount.create(id = cf_username, person_id = person_id)
    person = await PushPerson.filter(id = person_id).first()
    if not person:
        await PushPerson.create(id = person_id, open = True)
    await push.send("绑定 cf 账号成功")
    
async def push_unbind(cf_username):
    if account := await PushAccount.filter(id = cf_username).first():
        person_id = account.person_id
        await account.delete()
        if not await PushAccount.filter(person_id = person_id).exists():
            person = PushPerson.filter(id = person_id)
            await person.delete()
        await push.send("解绑 cf 账号成功")
    else:
        await push.send("该 cf 账号未被绑定过")


async def query_person_pushed(person_id):
    if person := await PushPerson.filter(id = person_id).first():
        if not person.open:
            return []
    else:
        return []
    accounts = await PushAccount.filter(person_id = person_id)
    return [account.id for account in accounts]

def get_recent_solved(username, td):
    url = "https://codeforces.com/api/user.status?handle=" + username
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("code %d" % resp.status_code)
    now_time = datetime.now()
    problems = []
    for record in resp.json()["result"]:
        if now_time - td > datetime.fromtimestamp(record["creationTimeSeconds"]):
            break
        problems.append(record["problem"])
    return problems

def no_zero_div(x, y):
    return x / y if y != 0 else 0

async def push_with_day(group_id, day, at):
    bot = get_bot()
    members = await bot.get_group_member_list(group_id = group_id)
    dic = {}
    msg = ""
    for member in members:
        accounts = await query_person_pushed(member["user_id"])
        if len(accounts) == 0:
            continue
        cnt = rated_cnt = rated_sum = 0
        solved = []
        for account in accounts:
            try:
                acc_solved = get_recent_solved(account, timedelta(days = day))
            except Exception as e:
                await bot.call_api("send_group_msg", group_id = group_id, message = str(e))
                return
            solved += acc_solved
        solved = [json.loads(item) for item in {json.dumps(d) for d in solved}]
        for problem in solved:
            cnt += 1
            if "rating" in problem:
                rated_cnt += 1
                rated_sum += problem["rating"]
        dic[json.dumps(member, sort_keys = True)] = (cnt, rated_cnt, rated_sum)
    sorted_dic = dict(sorted(dic.items(), key = lambda x: (x[1][0], no_zero_div(x[1][2], x[1][1])), reverse = True))
    rk = 0
    for memberstr, value in sorted_dic.items():
        member = json.loads(memberstr)
        rk += 1
        name = member["card"] if len(member["card"]) > 0 else member["nickname"]
        msg += "#%d %s  %d题 平均 rating: " % (rk, name, value[0])
        if value[1] == 0:
            msg += "?\n"
        else:
            msg += "%d\n" % round(value[2] / value[1])
    await bot.call_api("send_group_msg", group_id = group_id, message = msg)
    if at:
        msg = Message()
        need_push_num = len(sorted_dic) // 2
        reversed_dic = {key: sorted_dic[key] for key in reversed(list(sorted_dic.keys()))}
        las = -1
        for memberstr, value in reversed_dic.items():
            if need_push_num <= 0 and value[0] != las:
                break
            member = json.loads(memberstr)
            msg += MessageSegment.at(member["user_id"]) + " "
            need_push_num -= 1
            las = value[0]
        msg += "该加训了！！"
        await bot.call_api("send_group_msg", group_id = group_id, message = msg)