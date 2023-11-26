import requests

# r = requests.post("http://82.156.5.141:8000/api/user/register",json={
#     "username": 1231222223,
#     "password": "asddsa",
#     "device_id": "",
# })

# print(r.text)


# r = requests.post("http://82.156.5.141:8000/api/user/login",json={
#     "username": 1231222223,
#     "password": "asddsa",
#     "device_id": '5'
# })

# print(r.text)

# r = requests.post("http://82.156.5.141:8000/api/video/add_group",
#                  json={
#                     "name": "测试",
#                  },
#                  headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDEwMjI1OTV9.XWXYFxzQVzhayNrykyKZTtrq6t5ZYe-RITiBTJj7TtE"}).text
# print(r)

# # # r = requests.get("http://82.156.5.141:8000/api/video/group",
# # #                   headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5Mjc1OTl9.4kR2Oc_nb_RGtEv-t32U-exc1CVD-AntraUp8VNYaYg"}).text
# # # print(r)


# # # r = requests.post("http://82.156.5.141:8000/api/video/del_group",
# # #                  json={
# # #                      "id": 1
# # #                  },
# # #                  headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5MjQ0NjF9.3iOdvhfD5F_PTa4OvQeKvXinTzyqwgqS4MU8iHN_Zvw"}).text
# # # print(r)



r = requests.post("http://82.156.5.141:8000/api/video/add_tag",json={
    "tag_name": "米饭",
    "keywords": ["啥","吃"],
    "group_id":  1,
    "voice_link": "http://www.baidu.com"
},
 headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDEwMjMxMTF9.vcxddBfPUU9JpNmTT8wvMSCh6cHoTNxjZOrXSpDsqhA"}

)
print(r.text)
# # print(r.text)
# # r = requests.get("http://82.156.5.141:8000/api/video/tag/group_id=1",
# #  headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5NTU0MjJ9.GSjDZEnRDnCpcoTyb1m7yE1PhaAcQvtiSOyI0vv8j1A"}

# # )
# r = requests.post("http://82.156.5.141:8000/api/video/add_word",
#                     json={
#                      "tag_id": 2,
#                      "group_id":1,
#                      "word": "你好"
#                  },
#  headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjUiLCJleHAiOjE3MDA5NTU0NzJ9.B5TuFr_zJWuxikn7sgNEW4jK86mXooCbN-zzu7ykrg0"}

# )

print(r.text)
