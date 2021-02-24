import requests


res = requests.post("http://localhost/pose", data={"text": "cry", "_csrf_token": ""})
print(res.content.decode("utf-8"), res.status_code)