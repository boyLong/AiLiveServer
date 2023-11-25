import requests

# r = requests.post("http://127.0.0.1:8000/api/user/register",json={
#     "username": 1231222223,
#     "password": "asddsa",
#     "device_id": ''
# })

# print(r.text)


r = requests.post("http://127.0.0.1:8000/api/user/login",json={
    "username": 1231222223,
    "password": "asddsa",
    "device_id": '5'
})

print(r.text)

# r = requests.post("http://127.0.0.1:8000/api/video/add_group",
#                  json={
#                     "name": "测试机",
#                  },
#                  headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5MjQ0NjF9.3iOdvhfD5F_PTa4OvQeKvXinTzyqwgqS4MU8iHN_Zvw"}).text
# print(r)

r = requests.post("http://127.0.0.1:8000/api/video/del_group",
                 json={
                     "id": 1
                 },
                 headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5MjQ0NjF9.3iOdvhfD5F_PTa4OvQeKvXinTzyqwgqS4MU8iHN_Zvw"}).text
print(r)

