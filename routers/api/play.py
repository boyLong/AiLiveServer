import re
import hashlib

from urllib import parse
import httpx
from fastapi import APIRouter,Depends
from schemas.Response import ResponseBase
from schemas.Live import LiveBase,LiveWsBase
from schemas.User import UserInfoBase
from config import STATUS
from common.auth import check_jwt_token
from common.spider import DySPider
import time
router = APIRouter()

@router.post("/live_info",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg","data"])
async def live_info(live: LiveBase, user: UserInfoBase = Depends(check_jwt_token)):
    """获取直播间信息"""
    url =re.findall(
    "(https://.*?)\s",
    live.live
)   
    if not url:
        return {"status":STATUS.ERROR,"msg": "直播间地址解析失败"}
    try:
        dy = DySPider(userAgent=live.UserAgent,url=url)
        info = await dy.info()
    except Exception as e:
        print(e)
        return {"status":STATUS.ERROR,"msg": "系统出错,请重试",}
    return {"status":STATUS.SUCCESS,"msg": "成功", "data": info}


@router.post("/live_ws", response_model=ResponseBase,response_model_include=["status","msg","data"])
async def live_ws(live: LiveWsBase, ):
    room_id = live.room_id
    user_unique_id = live.user_unique_id
    first_time = live.time
    fetch_time = int(time.time()* 1000)
    internal_ext = f'''internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:{user_unique_id}|dim_log_id:|first_req_ms:{first_time}|fetch_time:{fetch_time}|seq:1|wss_info:0-{fetch_time}-0-0|wrds_kvs:WebcastRoomStatsMessage-_WebcastRoomRankMessage-'''
    data = {
    "app_name": "douyin_web",
    "version_code": "180800",
    "webcast_sdk_version": "1.0.12",
    "update_version_code": "1.0.12",
    "compress": "gzip",
    "device_platform": "web",
    "cookie_enabled": "true",
    "screen_width": "1920",
    "screen_height": "1080",
    "browser_language": "zh-CN",
    "browser_platform": "Win32",
    "browser_name": "Mozilla",
    "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "browser_online": "true",
    "tz_name": "Asia/Shanghai",
    "cursor": "u-1_h-1_t-{fetch_time}_r-_rdc-1_d-1",
    "internal_ext": internal_ext,
    "host": "https://live.douyin.com",
    "aid": "6383",
    "live_id": "1",
    "did_rule": "3",
    "endpoint": "live_pc",
    "support_wrds": "1",
    "user_unique_id": str(user_unique_id),
    "im_path": "/webcast/im/fetch/",
    "identity": "audience",
    "need_persist_msg_count": "15",
    "room_id": str(room_id),
    "heartbeatDuration": "0",
   
    }
    string = f"live_id=1,aid=6383,version_code=180800,webcast_sdk_version=1.0.12,room_id={room_id},sub_room_id=,sub_channel_id=,did_rule=3,user_unique_id={user_unique_id},device_platform=web,device_type=,ac=,identity=audience"
    sign = hashlib.md5(string.encode()).hexdigest()
    print(sign)
    async with httpx.AsyncClient() as s:

        resp = await s.post("http://127.0.0.1:6699/dy/sign",data={"sign":sign})
        resp = resp.json()
    data["signature"] = resp["result"]
    ws_url = "wss://webcast5-ws-web-hl.douyin.com/webcast/im/push/v2/?"+parse.urlencode(data)

    return {"status": STATUS.SUCCESS, "msg": "成功", "data":{"ws_url":ws_url}}