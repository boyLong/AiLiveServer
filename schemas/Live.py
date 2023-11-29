
from pydantic import BaseModel


# Shared properties
class LiveBase(BaseModel):
    live: str
    UserAgent: str='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


class LiveWsBase(BaseModel):
    room_id: str
    user_unique_id: str
    time: int
    
