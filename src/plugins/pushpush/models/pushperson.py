from tortoise import fields
from tortoise.models import Model
from nonebot_plugin_tortoise_orm import add_model

class PushPerson(Model):
    id = fields.IntField(pk = True)
    cf_username = fields.CharField(max_length = 25, null = True)
    open = fields.BooleanField()
    class Meta:
        table = "pushperson"
        table_description = "记录每个群组中有谁在加训模式当中"

add_model("src.plugins.pushpush.models.pushperson")