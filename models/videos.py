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
    # Word = fields.CharEnumField
    user = fields.ForeignKeyField("models.UserModel",on_delete=fields.CASCADE,related_name="group_user")

class ReplyTagModel(Model):
    id = fields.IntField(pk=True, index=True)
    tag = fields.CharField(max_length=255,)
    category = fields.CharField(max_length=255,)
    word = fields.CharEnumField(WordEnum,max_length=255,description="匹配关键词")
    VideoLink = fields.CharField(max_length=10,description="视频链接")
    group_name = fields.ForeignKeyField("models.GroupModel", on_delete=fields.CASCADE,related_name="group_name")


class VoiceModel(Model):
    id = fields.IntField(pk=True, index=True)
    VideosLink = fields.CharField(max_length=255,)