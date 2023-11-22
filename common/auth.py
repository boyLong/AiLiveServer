import jwt
from typing import Optional
from fastapi import Header,HTTPException
from datetime import datetime,timedelta
from passlib.context import CryptContext
from config import SECRET_KEY,ALGORITHM
from pydantic import ValidationError
from models.user import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    哈希来自用户的密码
    :param password: 原密码
    :return: 哈希后的密码
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    校验接收的密码是否与存储的哈希值匹配
    :param plain_password: 原密码
    :param hashed_password: 哈希后的密码
    :return: 返回值为bool类型，校验成功返回True,反之False
    """
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """

    :param data: 需要进行JWT令牌加密的数据（解密的时候会用到）
    :param expires_delta: 令牌有效期
    :return: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # 添加失效时间
    to_encode.update({"exp": expire})
    # SECRET_KEY：密钥
    # ALGORITHM：JWT令牌签名算法
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_jwt_token(token: Optional[str] = Header("")):
    """
    验证token
    :param token:
    :return: 返回用户信息
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        # 通过解析得到的username,获取用户信息,并返回
        return await UserModel.filter(username=username).first().values("id","username",  "is_allow","created_at","updated_at","Expire_at")
 
    except Exception as e:
        print(e)
        print(e.args)
        raise HTTPException(
            status_code=401,
            detail={
                'code': 5000,
                'message': "Token Error",
                'data': "Token Error",
            }
        )