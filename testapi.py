import  requests

r = requests.post("http://82.156.5.141:8000/api/video/upload",files={
    "file": open(r"E:\work\AiLiveServer\requirements.txt")
})
print(r.text)