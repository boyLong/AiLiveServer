import requests

r = requests.post("http://127.0.0.1:8000/user/register",json={
    "username": 1231222223,
    "password": "asddsa"
})

print(r.text)


# r = requests.post("http://127.0.0.1:8000/user/login",json={
#     "username": 1231223,
#     "password": "assa"
# })

# print(r.text)

# r = requests.get("http://127.0.0.1:8000/user/info",headers={"token":"eybGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjMsImV4cCI6MTcwMTI3ODc1OX0.c_1MRnAD3OFgULA7EQ9W91a3An3LHm681tg6kMtZzFc"}).text
# print(r)