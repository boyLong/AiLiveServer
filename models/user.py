from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.BigIntField(index=True, description="用户手机号")
    # 与django不同的是，这里的description可以直接在数据库表中看到哦。
    password = fields.CharField(max_length=255, description="用户密码")  # 密码不要存明文，存hash值。
    is_allow = fields.BooleanField(default=False, description="是否能用")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    Expire_at = fields.DatetimeField(auto_now_add=True, description="到期时间")
    
    class Meta:
        table = "user"  # 数据库中的表名称

class ExCodeModel(Model):
    id = fields.IntField(pk=True, index=True)
    code = fields.CharField(max_length=255,index=True,  description="激活码")
    used = fields.BooleanField(default=False, description="是否使用过")
    ex_time = fields.IntField(default=False, description="可用天数")
    remark = fields.CharField(max_length=255, description="备注")
    user = fields.ForeignKeyField("models.UserModel",on_delete=fields.CASCADE,related_name="user")

    class Meta:
        table = "Ex_Code"  # 数据库中的表名称