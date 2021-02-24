import requests


res = requests.post("http://localhost/pose", data={"text": "cry", "_csrf_token": "what"})
print(res.content.decode("utf-8"), res.status_code)

headers = {
    "referer": "http://127.0.0.1/"
}

res = requests.post("http://localhost/pose", data={"text": "laugh", "_csrf_token": "why"}, headers=headers)
print(res.content.decode("utf-8"), res.status_code)