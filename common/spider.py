import re
import httpx



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
        return {"web_rid":web_rid, "title":title, "room_id":room_id,"url": f"https://live.douyin.com/{web_rid}"}


if __name__ == "__main__":
    import asyncio
    a = DySPider(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "https://v.douyin.com/iRWDaDYD/",
    )

    info = asyncio.run(a.info())
    print(info)
