import requests

r = requests.post("http://127.0.0.1:8000/api/user/register",json={
    "username": 1231222223,
    "password": "asddsa",
    "device_id": ''
})

print(r.text)


r = requests.post("http://127.0.0.1:8000/api/user/login",json={
    "username": 1231222223,
    "password": "asddsa",
    "device_id": '5'
})

print(r.text)

r = requests.get("http://127.0.0.1:8000/api/user/info",headers={'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzEyMjIyMjMsImRldmljZV9pZCI6IjMiLCJleHAiOjE3MDA5MjM5MzN9.9Pr2tU5GLcwcSk9nl50ZIBSO4lp5w-_hef_skIy2aHg"}).text
print(r)