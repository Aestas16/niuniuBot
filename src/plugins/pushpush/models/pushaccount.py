from tortoise import fields
from tortoise.models import Model
from nonebot_plugin_tortoise_orm import add_model

class PushAccount(Model):
    id = fields.CharField(max_length = 25, pk = True)
    person_id = fields.IntField()
    class Meta:
        table = "pushaccount"
        table_description = "记录每个号的 owner"


add_model("src.plugins.pushpush.models.pushaccount")