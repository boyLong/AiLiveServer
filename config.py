SECRET_KEY = "eac77e4e9a9a767b792779132e84ea37b1f4c31bec56714607f617a3fbdfbd53"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 10


TORTOISE_ORM = {
    "connections": {"default": "mysql://root:981022989aa92fc0@82.156.5.141:3306/ailive"},
    "apps": {
        "models": {
            "models": ["models.user","models.videos", "aerich.models"],
            "default_connection": "default",
        },
    },
    "routers": [],
    "use_tz": False,
    "timezone": "UTC"
}


class STATUS:
    ERROR = 500
    SUCCESS = 200


# FILE_PATH = "/ai-data"
FILE_PATH = r"C:/Users/13106\Desktop/app"