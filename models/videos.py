from tortoise import fields
from tortoise.models import Model
from models.user import UserModel
from enum import Enum



class WordEnum(list, Enum):
	word = ""

#  智能回复
class GroupModel(Model):
    id = fields.IntField(pk=True, index=True)
    
    groupName = fields.CharField(max_length=255,)
    user = fields.ForeignKeyField("models.UserModel",on_delete=fields.CASCADE,related_name="group_user")

class ReplyTagModel(Model):
    id = fields.IntField(pk=True, index=True)
    tag_name = fields.CharField(max_length=255,)
    keywords = fields.JSONField(description="匹配关键词")
    voice_link = fields.TextField(description="视频链接")
    group_id = fields.ForeignKeyField("models.GroupModel", on_delete=fields.CASCADE,related_name="group_id")


class VoiceModel(Model):
    id = fields.IntField(pk=True, index=True)
    VideosLink = fields.CharField(max_length=255,)