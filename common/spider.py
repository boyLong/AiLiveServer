import re
import httpx
import time



class AcSignature():
    def __init__(self, ua, url, __ac_nonce):
        self.ua = ua
        self.url = url
        self.__ac_nonce = __ac_nonce
        self.canvas_hash = 1978764126

    def int_overflow(self,val):
        '''判断移位操作是否需要溢出,主要是解决python左移操作不会溢出成-482315155这种'''
        maxint = 2147483647
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    def unsigned_right_shift(self, signed, i=0):
        '''
        python实现无符号右移
        :param signed: 待操作对象
        :param i: 右移位数，默认移动0位
        :return:
        '''
        shift = signed % 0x100000000
        return shift >> i

    def sdb_hash(self, string, hash=0):
        '''
        SDBMHash算法，魔改时hash初始值变化
        :param string: 待加密字符串
        :param hash: hash初始值
        :return:
        '''
        for char in string:
            hash = self.unsigned_right_shift((hash ^ ord(char)) * 65599, 0)
        return hash

    def sdb_hash2(self,string, hash=0):
        for char in string:
            hash = self.unsigned_right_shift((hash * 65599 + ord(char)), 0)
        return hash

    def move_char_calc(self, nor):
        '''根据nor的值判断移动的位数，避免charCode取到特殊字符'''
        if 0 <= nor < 26:
            char_at = nor + 65
        elif 26 <= nor < 52:
            char_at = nor + 71
        elif nor == 62 or nor == 63:
            char_at = nor - 17
        else:
            char_at = nor - 4
        char = chr(char_at)
        return char

    def get_long_numer(self, url: str):
        '''获取长整数 * 长整数用于各组加密'''
        timestamp = int(time.time())
        timestamp_hash = self.sdb_hash(str(timestamp), 0)
        self.url_hash = self.sdb_hash(url, timestamp_hash)
        xor_num = timestamp ^ ((self.url_hash % 65521) * 65521)
        xor_num = self.unsigned_right_shift(xor_num,0)
        bin_xor_num = bin(xor_num).replace("0b","") if len(bin(xor_num).replace("0b","")) == 32 else "0" *(32 - len(bin(xor_num).replace("0b",""))) + bin(xor_num).replace("0b","")
        binary = f"{10000000110000}{bin_xor_num}".replace("0b", "")
        long_number = int(binary, 2)
        return long_number

    def char_to_signature2(self, long_number):
        string = ""
        offsets = [24, 18, 12, 6, 0]
        for offset in offsets:
            nor = long_number >> 2 >> offset & 63
            string += self.move_char_calc(nor)
        return string

    def char_to_signature3(self, long_number):
        string = ""
        offsets = [24, 18, 12, 6, 0]
        for offset in offsets:
            nor = (long_number << 28 ^ 515) >> offset & 63
            string += self.move_char_calc(nor)
        return string

    def char_to_signature4(self, long_number):
        string = ""
        offsets = [24, 18, 12, 6, 0]
        for offset in offsets:
            nor = (-1073741824 ^ self.unsigned_right_shift(long_number ^ self.canvas_hash, 6)) >> offset & 63 # 家里的
            # nor = (-1073741824 ^ self.unsigned_right_shift(long_number ^ 536919696, 6)) >> offset & 63 # 公司的
            string += self.move_char_calc(nor)
        return string

    def char_to_signature6(self, long_number, ua, __ac_nonce):
        offsets = [24, 18, 12, 6, 0]
        # 对长整数进行hash计算
        long_number_hash = self.sdb_hash(str(long_number),0)
        # 对ua进行hash计算
        self.ua_hash = self.sdb_hash(self.ua,long_number_hash)
        self.__ac_nonce_hash = self.sdb_hash(__ac_nonce, long_number_hash)
        string = ""
        for offset in offsets:
            nor = (((self.ua_hash % 65521 << 16) ^ (self.__ac_nonce_hash % 65521)) >> 2 >> offset & 63)
            string += self.move_char_calc(nor)
        return string

    def char_to_signature7(self, long_number):
        offsets = [24, 18, 12, 6, 0]
        string = ""
        xor1 = (self.int_overflow(self.ua_hash % 65521 << 16) ^ self.__ac_nonce_hash % 65521) << 28
        xor2 = self.unsigned_right_shift(long_number ^ 540960, 4) # 家里是16672
        # xor2 = self.unsigned_right_shift(long_number ^ 288, 4)  # 公司是288
        for offset in offsets:
            nor = (xor1 ^ xor2) >> offset & 63
            string += self.move_char_calc(nor)
        return string

    def char_to_signature8(self):
        offsets = [24, 18, 12, 6, 0]
        string = ""
        for offset in offsets:
            nor = (self.url_hash % 65521) >> offset & 63
            string += self.move_char_calc(nor)
        return string

    def char_to_signature9(self, sig):
        sig_hash = self.sdb_hash2(sig,hash=0)
        return hex(sig_hash).replace("0x","")[-2:]


    def get_signature(self):
        '''获取signature'''
        sig1 = "_02B4Z6wo00001" # TODO
        sig1 = "_02B4Z6wo00f01"
        # 获取长整数
        long_number = self.get_long_numer(self.url)
        sig2 = self.char_to_signature2(long_number)
        sig3 = self.char_to_signature3(long_number)
        sig4 = self.char_to_signature4(long_number)
        sig5 = self.move_char_calc((long_number ^ self.canvas_hash) & 63)
        sig6 = self.char_to_signature6(long_number,self.ua, self.__ac_nonce)
        sig7 = self.char_to_signature7(long_number)
        sig8 = self.char_to_signature8()
        sig9 = self.char_to_signature9(sig1 + sig2 + sig3 + sig4 + sig5 + sig6 + sig7 + sig8)
        ac_signature = sig1 + sig2 + sig3 + sig4 + sig5 + sig6 + sig7 + sig8 + sig9
        return ac_signature
class DySPider:
    def __init__(self, userAgent, url, proxy=None) -> None:
        self.userAgent = userAgent
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.userAgent,
        }

        self.session = httpx.AsyncClient(headers=headers, http2=True, proxies=proxy)
        self.url = url

    async def room_id(self):
        resp = await self.session.get(
            self.url,
            # follow_redirects=False,
        )
        url = resp.headers.get("location")
        room_id = re.findall("room_id=(\d+)", url)
        return room_id[0]

    async def info(
        self,
    ):
        room_id = await self.room_id()

        query = f"verifyFp=&type_id=0&live_id=1&room_id={room_id}&sec_user_id=&version_code=99.99.99&app_id=1128&msToken="

        x_b = await self.session.post(
            "http://127.0.0.1:6699/dy/xb",
            data={"query": query, "user_agent": self.userAgent},
            headers={},
        )

        response = await self.session.get(
            "https://webcast.amemv.com/webcast/room/reflow/info/?"
            + query
            + "&X-Bogus="
            + x_b.json()["result"],
        )
        data = response.json()
        web_rid = data["data"]["room"]["owner"]["web_rid"]
        title = data["data"]["room"]["title"]

        url = f"https://live.douyin.com/{web_rid}"
        
        response = await self.session.get(
            url
        )
        __ac_nonce = response.cookies.get("__ac_nonce")
        
        __ac_signature = AcSignature(self.userAgent, "live.douyin.com/{web_rid}", __ac_nonce,)
        __ac_signature = __ac_signature.get_signature()
        cookie = f"__ac_nonce={__ac_nonce}; __ac_signature={__ac_signature}; __ac_referer=__ac_blank"
        return {"web_rid":web_rid, "title":title, "room_id":room_id,"url": f"https://live.douyin.com/{web_rid}" ,"cookie": cookie}


if __name__ == "__main__":
    import asyncio
    a = DySPider(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "https://v.douyin.com/iRWDaDYD/",
    )

    info = asyncio.run(a.info())
    print(info)
