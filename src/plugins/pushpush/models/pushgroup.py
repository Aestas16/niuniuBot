from tortoise import fields
from tortoise.models import Model
from nonebot_plugin_tortoise_orm import add_model

class PushGroup(Model):
    id = fields.IntField(pk = True)
    open = fields.BooleanField()
    class Meta:
        table = "pushgroup"
        table_description = "记录每个群组是否开启压力加训模式"


add_model("src.plugins.pushpush.models.pushgroup")